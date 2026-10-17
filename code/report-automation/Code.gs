function main() {

  const templateId = '1COOLJTi7wIzspGQJyePTwZ-u61YuO-BkzrGe28QTfHc';
  
  const destinationFolderId = '1wFii4ymXCG244mFf4WuZ27cWtS8PuPpm'; //ENTER DESTINATION FOLDER ID HERE

  const request1 = { 
    name: "Vietnam", 
    parents: [destinationFolderId] 
  };
  
  const copiedFile = Drive.Files.copy(request1, templateId);
  const docId = copiedFile.id;

  const doc = Docs.Documents.get(docId);
  const inlineObjects = doc.inlineObjects || {};
  const altTextToIdMap = {};

  for (const [id, obj] of Object.entries(inlineObjects)) {
    const title = obj.inlineObjectProperties.embeddedObject.title;
    console.log(title)
    if (title) {
      altTextToIdMap[title] = id;
    }
  }

  const img_request = {
    "requests" : []
  }
  folder = DriveApp.getFolderById('19Wk5U4eMCVHf059zd0J8iqc-AqqJt85N'); //ENTER IMAGE FOLDER ID HERE
  //(MUST BE PUBLIC)
  files = folder.getFiles();
  while(files.hasNext()) {
    let file = files.next();
    let fileName = file.getName().slice(0,-4); // Assuming filename matches Alt Text title

    // Check if the filename exists as Alt Text in the doc
    if (altTextToIdMap[fileName]) {
      img_request["requests"].push({
        "replaceImage": {
          "imageObjectId": altTextToIdMap[fileName],
          "uri": `https://drive.usercontent.google.com/download?id=${file.getId()}`,
          "imageReplaceMethod": 'IMAGE_REPLACE_METHOD_UNSPECIFIED'
        }
      });
    }
  }

  if (img_request.requests.length > 0) {
    Docs.Documents.batchUpdate(img_request, docId);
  }

  const jsonfile = DriveApp.getFileById('1xS4hlMiKVnZHCqBCknjrPsH-McvOHdMy'); //ENTER JSON FILE ID HERE
  const textupdates = JSON.parse(jsonfile.getBlob().getDataAsString());
  const txt_request = {
    "requests" : []
  }

  for (const [key, value] of Object.entries(textupdates)) {
    txt_request["requests"].push(
      { "replaceAllText":
        {
          "replaceText": value.toString(),
          "containsText":
                        {
              "text": key,
              "matchCase": false
            }
        }
      }
    )
  }
  Docs.Documents.batchUpdate(txt_request, docId)

}


function batchProcessDocuments() {
  // --- CONFIGURATION ---
  const templateId = '1COOLJTi7wIzspGQJyePTwZ-u61YuO-BkzrGe28QTfHc';
  const destinationFolderId = '1wFii4ymXCG244mFf4WuZ27cWtS8PuPpm'; 
  const mainBatchFolderId = '1CAHX2oJ6YVfEWSPbkVd8KdWVeZOYEwgF'; // The folder containing all your subfolders

  const batchFolder = DriveApp.getFolderById(mainBatchFolderId);
  const subfolders = batchFolder.getFolders();

  // Iterate through each subfolder in the main batch folder
  while (subfolders.hasNext()) {
    const subfolder = subfolders.next();
    const docName = subfolder.getName(); // The subfolder name becomes the doc name
    
    Logger.log(`Processing folder: ${docName}`);

    // 1. Locate the 'img' folder and the '.json' file inside this subfolder
    let imgFolder = null;
    let jsonFile = null;

    const innerFolders = subfolder.getFoldersByName('img');
    if (innerFolders.hasNext()) {
      imgFolder = innerFolders.next();
    }

    const files = subfolder.getFiles();
    while (files.hasNext()) {
      const file = files.next();
      // Check if it's a JSON file (by MIME type or extension)
      if (file.getMimeType() === MimeType.JSON || file.getName().endsWith('.json')) {
        jsonFile = file;
        break; 
      }
    }

    // Skip this folder if it's missing required components
    if (!imgFolder || !jsonFile) {
      Logger.log(`Skipping "${docName}": Missing 'img' folder or '.json' file.`);
      continue;
    }

    // 2. Create the document from template
    const copyRequest = { 
      name: docName, 
      parents: [destinationFolderId] 
    };
    const copiedFile = Drive.Files.copy(copyRequest, templateId);
    const docId = copiedFile.id;

    // 3. Get document inline objects to map Alt Text titles to IDs
    const doc = Docs.Documents.get(docId);
    const inlineObjects = doc.inlineObjects || {};
    const altTextToIdMap = {};

    for (const [id, obj] of Object.entries(inlineObjects)) {
      const title = obj.inlineObjectProperties.embeddedObject.title;
      if (title) {
        altTextToIdMap[title] = id;
      }
    }

    // 4. Process Images
    const img_request = { "requests" : [] };
    const imgFiles = imgFolder.getFiles(); // (Images MUST BE PUBLIC for the URI method to work)
    
    while(imgFiles.hasNext()) {
      let file = imgFiles.next();
      // Safely strip the extension regardless of length (e.g., .png or .jpeg)
      let fileName = file.getName().replace(/\.[^/.]+$/, ""); 

      // Check if the filename exists as Alt Text in the doc
      if (altTextToIdMap[fileName]) {
        img_request["requests"].push({
          "replaceImage": {
            "imageObjectId": altTextToIdMap[fileName],
            "uri": `https://drive.usercontent.google.com/download?id=${file.getId()}`,
            "imageReplaceMethod": 'IMAGE_REPLACE_METHOD_UNSPECIFIED'
          }
        });
      }
    }

    // Execute image replacement batch update
    if (img_request.requests.length > 0) {
      Docs.Documents.batchUpdate(img_request, docId);
    }

    // 5. Process Text
    const textupdates = JSON.parse(jsonFile.getBlob().getDataAsString());
    const txt_request = { "requests" : [] };

    for (const [key, value] of Object.entries(textupdates)) {
      txt_request["requests"].push({ 
        "replaceAllText": {
          "replaceText": value.toString(),
          "containsText": {
            "text": key,
            "matchCase": false
          }
        }
      });
    }

    // Execute text replacement batch update
    if (txt_request.requests.length > 0) {
      Docs.Documents.batchUpdate(txt_request, docId);
    }

    Logger.log(`Successfully generated document: ${docName}`);
  }
  
  Logger.log('Batch processing complete.');
}


function logTemplateImageIds() {
  const templateId = '1COOLJTi7wIzspGQJyePTwZ-u61YuO-BkzrGe28QTfHc';
  
  try {
    const doc = Docs.Documents.get(templateId);
    const inlineObjects = doc.inlineObjects;

    if (!inlineObjects) {
      console.log("No images found in this document.");
      return;
    }

    console.log("--- START OF IMAGE LIST ---");
    for (const [id, obj] of Object.entries(inlineObjects)) {
      const embeddedObject = obj.inlineObjectProperties.embeddedObject;
      const title = embeddedObject.title || "(No Alt Text Title)";
      
      console.log(`Image ID: ${id}`);
      console.log(`  > Alt Text: ${title}`);
    }
    console.log("--- END OF IMAGE LIST ---");
    
  } catch (e) {
    console.log("Error: " + e.message);
  }
}




