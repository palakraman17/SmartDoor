package com.amazonaws.samples;

import java.util.LinkedHashMap;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level; 
import java.util.logging.Logger;

public class CreateStreamProcessor {

	public void myHandler(LinkedHashMap<Object,Object> lhm) {
		// TODO Auto-generated method stub
		final Logger LOGGER = Logger.getLogger(Logger.GLOBAL_LOGGER_NAME); 
		
		String streamProcessorName="StreamProcessor2";
    	String kinesisVideoStreamArn="arn:aws:kinesisvideo:us-east-1:665243609809:stream/KVS1/1572463603671";
    	String kinesisDataStreamArn="arn:aws:kinesis:us-east-1:665243609809:stream/AmazonRekognitionKDS1";
    	String roleArn="arn:aws:iam::665243609809:role/RekognitionRole";
    	String collectionId="Collection";
    	Float matchThreshold=80F;
    	
    	LOGGER.log(Level.INFO, "before createStreamProcessor()");
		try {
			StreamManager sm= new StreamManager(streamProcessorName,kinesisVideoStreamArn,kinesisDataStreamArn,roleArn,collectionId,matchThreshold);
			/*
			sm.createStreamProcessor();
			System.out.println("After calling createStreamProcessor()");
			LOGGER.log(Level.INFO, "After calling createStreamProcessor()");
			*/
			/*
			sm.startStreamProcessor();
			//LOGGER.log(Level.INFO, "After startStreamProcessor()");  
			*/
			//TimeUnit.SECONDS.sleep(60);
			/*
			sm.listStreamProcessors();
			LOGGER.log(Level.INFO, "After listStreamProcessor()"); 
			*/
			/*
			sm.stopStreamProcessor();
			LOGGER.log(Level.INFO, "After stopStreamProcessor()");  
			*/
			/*
			sm.deleteStreamProcessor();
			LOGGER.log(Level.INFO, "After deleteStreamProcessor()"); 
			*/
		}
		catch(Exception e){
			LOGGER.log(Level.INFO, e.getMessage()); 
			
			System.out.println(e.getMessage());
		}
	}

}



