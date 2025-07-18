from pyspark.sql import SparkSession, functions
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit
from pyspark.ml.evaluation import RegressionEvaluator
import ast
import fasttext

spark = SparkSession.builder.master("local[1]").appName("SparkApp").getOrCreate()
fasttext_model = fasttext.load_model("models/cc.en.300.bin")


def load_data(file_path):
    """
    Load data from a CSV file into a Spark DataFrame.
    """
    def parse_vector(vector_str):
        """
        Parse a string representation of a vector into a list of floats.
        """
        return Vectors.dense(ast.literal_eval(vector_str))
    
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    
    df = df.withColumn("vector", functions.udf(parse_vector, VectorUDT())("vector"))

    return df


def process_data(df):
    """
    Process the DataFrame by filtering and selecting relevant columns.
    """
    # scaler = StandardScaler(inputCol="num_comments", outputCol="norm_comm")
    # df = scaler.fit(df).transform(df)
    # df.show(5)
    # exit(0)

    # # Convert to vector
    vector_assembler = VectorAssembler(inputCols=["vector"], outputCol="features")
    df = vector_assembler.transform(df)

    # # rename score to label
    df = df.withColumnRenamed("score", "label")

    return df.select("label", "features")


def train_model(df):
    """
    Train a machine learning model using the processed DataFrame.
    """
    lr = LinearRegression(maxIter=100)
    paramGrid = ParamGridBuilder()\
        .addGrid(lr.regParam, [0.1, 0.05, 0.01])\
        .addGrid(lr.elasticNetParam, [0, 0.5, 1])\
        .addGrid(lr.fitIntercept, [True, False])\
        .build()

    tvs = TrainValidationSplit(estimator=lr,
                              estimatorParamMaps=paramGrid,
                              evaluator=RegressionEvaluator(),
                              trainRatio=0.8)
    
    model = tvs.fit(df).bestModel
    return model


def evaluate_model(model, df):
    """
    Evaluate the trained model using the test DataFrame.
    """
    predictions = model.transform(df)
    evaluator = RegressionEvaluator()
    rmse = evaluator.evaluate(predictions, {evaluator.metricName: "rmse"})
    mse = evaluator.evaluate(predictions, {evaluator.metricName: "mse"})
    r2 = evaluator.evaluate(predictions, {evaluator.metricName: "r2"})
    
    return {
        "rmse": rmse,
        "mse": mse,
        "r2": r2
    }


def predict(model, text):
    """
    Predict using the trained model.
    """
    vector = fasttext_model.get_sentence_vector(text).tolist()

    vector = Vectors.dense(vector)
    vector = spark.createDataFrame([(vector,)], ["features"])

    predictions = model.transform(vector)
    
    return predictions.select("prediction").collect()


if __name__ == "__main__":
    # Load data
    df = load_data("posts.csv")
    
    # Process data
    processed_df = process_data(df)
    train_set, test_set = processed_df.randomSplit([0.8, 0.2], seed=42)
    
    print(f"DataFrame Schema: {train_set.show(5)}")
    # Train model
    model = train_model(train_set)
    model.write().overwrite().save("models/spark_model")
    
    # Evaluate model
    evaluation_results = evaluate_model(model, test_set)
    print(f"Evaluation Results: {evaluation_results}")

    text_to_predict = "Crabs don't have a brain, but they can still learn. Study shows."

    prediction = predict(model, text_to_predict)
    print(f"Prediction: {prediction[0][0]}")
    