#!/bin/bash

echo "🗑️  Terminating Elastic Beanstalk environment ..."
eb terminate microservice-orders --force || {
	echo "❌ Error occurred while terminating Elastic Beanstalk environment"
	exit 1
}
echo "✅ Done"
