#!/bin/bash

AWS_REGION=$(aws configure get region)

if [ ! -d ".elasticbeanstalk" ]; then
	echo "⚙️  Initializing Elastic Beanstalk Environment ..."
	eb init -p python-3.12 microservice-orders --region ${AWS_REGION} || {
		echo "❌ Error occurred while initializing Elastic Beanstalk Environment"
		exit 1
	}
	echo "✅ Done"
else
	echo "⏭️  Elastic Beanstalk already initialized, skipping ..."
fi

if ! eb status microservice-orders &>/dev/null; then
	echo "📦 Creating Elastic Beanstalk Environment ..."
	eb create microservice-orders || {
		echo "❌ Error occurred while creating Elastic Beanstalk Environment"
		exit 1
	}
	echo "✅ Done"
else
	echo "⏭️  Elastic Beanstalk environment already exists, skipping ..."
fi

echo "🚀 Deploying to Elastic Beanstalk Environment ..."
eb deploy || {
	echo "❌ Error occurred while deploying to Elastic Beanstalk Environment"
        exit 1
}
echo "✅ Done"
