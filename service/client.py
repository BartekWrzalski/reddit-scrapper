import grpc

from service.protobuf import project_pb2, project_pb2_grpc


TEXTS = [
    "Researchers at the University of Michigan have used CRISPR gene editing to restore hearing in mice with a congenital mutation. The team says this approach could be used to treat a form of hereditary deafness in humans, pending clinical trials.",
    "A peer-reviewed study of 62 human placentas found microplastics in 100% of samples, suggesting pervasive contamination of the human body from environmental exposure. Researchers are calling for urgent investigation into potential long-term effects.",
    "A team from a German research institute has developed a novel enzyme that can degrade polystyrene, one of the most difficult plastics to recycle. The enzyme works at room temperature and neutral pH, making it potentially scalable for industrial use.",
    "In a controlled experiment, children with ADHD performed significantly better on memory tasks after walking in a natural park compared to an urban setting. The findings support nature exposure as a complementary intervention.",
    "A paper published in Advanced Materials details how researchers achieved phase-aligned coupling between MoS₂ layers, potentially improving signal transduction in nanoscale optoelectronic devices. Application to quantum circuits remains theoretical.",
    "The model refines previous folding pathway predictions by introducing non-Euclidean metrics to better reflect actual energy states. Authors admit the work is preliminary but hope it inspires further investigation."
]


channel = grpc.insecure_channel("server:50051")
stub = project_pb2_grpc.SampleStub(channel)


for text in TEXTS:
    request = project_pb2.Request(value=text)
    response = stub.RunInference(request)
    print(response.value)
