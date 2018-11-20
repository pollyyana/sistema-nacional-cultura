pipeline {
	agent any
		node {
			checkout scm
			docker.withRegistry('registry.cultura.gov.br', 'credentials-id')
		}

	    stages {
		    stage('Build Docker Image') {
			    steps {
			    	echo 'Building image...'
			    	def sncImage = docker.build("sistema-nacional-cultura:${env.BUILD_ID}")
			    }
		    }
		    stage('Registry on Gitlab registry') {
			    steps {
				    echo 'Registering docker image on internal gitlab instance'
				    sh "docker login -u -p"

			    }

		    }
		    stage('Update development instance') {

		    }
	    }
}
