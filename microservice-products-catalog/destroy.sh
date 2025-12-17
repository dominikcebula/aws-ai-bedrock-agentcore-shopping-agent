#!/bin/bash

echo "🗑️  Terminating Elastic Beanstalk environment ..."
eb terminate microservice-products-catalog --force || {
	echo "❌ Error occurred while terminating Elastic Beanstalk environment"
	exit 1
}
echo "✅ Done"
