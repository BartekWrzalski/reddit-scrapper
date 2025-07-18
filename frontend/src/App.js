import logo from './logo.svg';
import './App.css';
import React from "react";

import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider,
  useQuery,
  gql
} from "@apollo/client";

const client = new ApolloClient({
  uri: '/graphql',
  cache: new InMemoryCache()
});

const PREDICT_QUERY = gql`
  query Predict($text: String!) {
    predictPopularity(text: $text) {
      score
    }
  }
`;

const PredictData = ({text}) => {
    const { loading, error, data } = useQuery(PREDICT_QUERY, {
        variables: { text },
        skip: !text // Skip query if text is not provided
    });
    console.log(data, loading, error);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;
    
    return (
        <div>
        <h2>Prediction Result</h2>
        <p>Score: {data?.predictPopularity.score}</p>
        </div>
    );
}

function App() {
    const [text, setText] = React.useState('');
    
    const handleInputChange = (event) => {
        setText(event.target.value);
    };
    
    return (
        <ApolloProvider client={client}>
        <div>
            <h1>Popularity Prediction v2</h1>
            <input
            type="text"
            value={text}
            onChange={handleInputChange}
            placeholder="Enter text to predict popularity"
            />
            <PredictData text={text} />
        </div>
        </ApolloProvider>
    );
}
export default App;