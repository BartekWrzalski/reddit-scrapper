from concurrent import futures
import time
from pyspark.ml.regression import LinearRegressionModel
import grpc
import fasttext
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors

from service.protobuf import project_pb2, project_pb2_grpc


fasttext_model = fasttext.load_model("models/cc.en.300.bin")
spark = SparkSession.builder.master("local[1]").appName("SparkApp").getOrCreate()
model = LinearRegressionModel.load("models/spark_model")


class SampleServicer(project_pb2_grpc.SampleServicer):
    def RunInference(self, request, context):
        print("Received inference request with input:", request.value)
        response = project_pb2.Response()

        vector = fasttext_model.get_sentence_vector(request.value).tolist()

        vector = Vectors.dense(vector)
        vector = spark.createDataFrame([(vector,)], ["features"])

        predictions = model.transform(vector)

        response.value = int(predictions.select("prediction").collect()[0][0])

        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
project_pb2_grpc.add_SampleServicer_to_server(SampleServicer(), server)

print("Starting server. Listening on port 50051.")
server.add_insecure_port("[::]:50051")
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
    print("Server stopped.")

