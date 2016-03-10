
pwservice_pb2.py: proto/pwservice.proto
	(cd proto/; protoc --python_out=.. --grpc_out=.. --plugin=protoc-gen-grpc=$(shell which grpc_python_plugin) pwservice.proto)
