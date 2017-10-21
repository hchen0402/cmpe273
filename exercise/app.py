from flask import Flask, request
import graphene, json

app = Flask(__name__)

class Query(graphene.ObjectType):
	hello = graphene.String()
	hi = graphene.Int()

	def resolve_hello(self, info, **args):
		return 'Hello'

schema = graphene.Schema(query=Query)
@app.route("/graphq1", methods=['POST'])

def graphq1():
	data = json.loads(request.data)
	return json.dumps(schema.execute(data['query']).data)


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')