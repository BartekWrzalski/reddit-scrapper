from ariadne import QueryType, make_executable_schema, gql, load_schema_from_path
from ariadne.asgi import GraphQL
import grpc
from service.protobuf import project_pb2, project_pb2_grpc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

query = QueryType()

@query.field("predictPopularity")
def resolve_predict_popularity(_, info, text):
    channel = grpc.insecure_channel("server:50051") 
    stub = project_pb2_grpc.SampleStub(channel)
    
    request = project_pb2.Request(value=text)
    response = stub.RunInference(request)

    return {"score": response.value}

type_defs = gql(load_schema_from_path("./service/schema.graphql"))
schema = make_executable_schema(type_defs, query)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_route("/graphql", GraphQL(schema, debug=True))
