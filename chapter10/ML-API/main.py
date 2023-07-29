# import the modules and localize them

from json import load as json_load
from google.cloud import storage, vision

storage_client = storage.Client()
vision_client = vision.ImageAnnotatorClient()

# open the buckets and localize them
with open('target.json') as json_data_file:
    buckets = json_load(json_data_file)

# Define cloud function "IMAGE_CHECKING"

def image_checking(data, context):
    # Read from input
    uri = "gs://" + data['bucket'] + "/" + data['name']
    image = vision.Image()
    image.source.image_uri = uri

    # Safe search using Cloud-Vision-API
    response = vision_client.safe_search_detection(image=image)
    result = response.safe_search_annotation
    print(result)

    # Check if the image is unsafe
    flagged = False
    for outcome in ['Likelihood.POSSIBLE', 'Likelihood.LIKELY', 'Likelihood.VERY_LIKELY']:
        if flagged == True:
            break
        for xresult in [
            result.adult, result.violence, result.racy]:
            if str(xresult) == str(outcome):
                flagged = True
                break
   # debug print(flagged)
    print("{}: {}".format(data['name'], result))

    # get the actual object_image from GCS
    gcsbucket = storage_client.get_bucket(data['bucket'])
    object_image = gcsbucket.get_blob(data['name'])

    # pick the new bucket based on how safe it is
    if flagged:
        newbucket = storage_client.get_bucket(buckets['UNSAFE_BUCKET'])
    else:
        newbucket = storage_client.get_bucket(buckets['SAFE_BUCKET'])

    # rewrite the image and delete the original
    newobject_image = newbucket.blob(data['name'])
    newobject_image.rewrite(object_image)
    object_image.delete()
