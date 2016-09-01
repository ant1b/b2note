import os, datetime, json
#from .models import *



def isvalidContext(fc=None):

    try:

        if fc and isinstance(fc,(str,list,dict)):

            if isinstance(fc, (str, unicode)) and len(fc)>0: return True

                

        else:

            print "Context field content is neither string nor list nor dict."
            return False

    except:

        print "isValidContext function failed."
        return False



def dispatchJsonFields( fieldname=None, fieldcontent=None ):

    try:

        if fieldname and isinstance(fieldname, (str, unicode)) and len(fieldname)>0:

            if fieldname == "@context": return isValidContext(fieldcontent)

            elif fieldname == "id": return isValidID(fieldcontent)

            elif fieldname == "target": return is ValidTarget(fieldcontent)

            elif fieldname == ""

        else:

            print "Provided json field name is not string or too short for being valid."
            return False

    except:

        print "dispatchJsonFields function failed"
        return False

    return True


def webAnnotationJsonValidationScript( ann_json=None ):

    try:

        if ann_json and isinstance(ann_json, (str, unicode)) and len(ann_json) > 0:

            try:

                json_o = json.loads( ann_json )

                if json_o and isinstance(json_o, dict):

                    allvalidfields = True

                    has_context = False

                    has_target = False

                    has_id = False

                    for fieldname in json_o.keys():

                        if fieldname and json_o[fieldname]:

                            dispatchJsonFields( fieldname, json_o[fieldname] )

                        else:

                            print "Invalid field, " + field + ", in dictionnary loaded from json."
                            allvalidfields = False
                            break

                    if not allvalidfields: return False

                else:

                    print "Provided object cannot be loaded as json in python."
                    return False

            except:

                print "Provided object cannot be loaded as json in python."
                return False

        else:

            print "Provided object is not string or too short for being valid json."
            return False

    except:

        pass
        return False

    return True



ann1 = '''{
      "body": [
        [
          {
            "type": [
              "TextualBody"
            ],
            "@id": "http://purl.obolibrary.org/obo/GAZ_00448034",
            "modified": "2016-08-31T11:17:09.705000",
            "value": "Loch Tralaig",
            "created": "2016-08-31T09:17:09.627000"
          }
        ]
      ],
      "target": [
        [
          {
            "@id": "https://b2share.eudat.eu/record/30",
            "modified": "2016-08-31T11:17:09.706000",
            "language": [
              "en"
            ],
            "created": "2016-08-31T09:17:09.627000"
          }
        ]
      ],
      "created": "2016-08-31T09:17:09.628000",
      "@id": "https://b2note.bsc.es/annotation/57c6bcb510d0600d435fa316",
      "modified": "2016-08-31T11:17:09.706000",
      "generated": "2016-08-31T09:17:09.628000",
      "@context": [
        "http://www.w3.org/ns/anno.jsonld"
      ],
      "type": [
        "Annotation"
      ]
    }'''

ann2 = '''{
      "body": [
        [
          {
            "type": [
              "TextualBody"
            ],
            "@id": "http://purl.uniprot.org/uniprot/P30249",
            "modified": "2016-08-31T13:09:37.401000",
            "value": "Locustatachykinin-3",
            "created": "2016-08-31T11:09:37.394000"
          }
        ]
      ],
      "target": [
        [
          {
            "@id": "https://b2share.eudat.eu/record/30",
            "modified": "2016-08-31T13:09:37.401000",
            "language": [
              "en"
            ],
            "created": "2016-08-31T11:09:37.394000"
          }
        ]
      ],
      "created": "2016-08-31T11:09:37.394000",
      "@id": "https://b2note.bsc.es/annotation/57c6d71110d0600f575c9f59",
      "modified": "2016-08-31T13:09:37.402000",
      "generated": "2016-08-31T11:09:37.394000",
      "@context": [
        "http://www.w3.org/ns/anno.jsonld"
      ],
      "type": [
        "Annotation"
      ]
    }
  ]
}'''



webAnnotationJsonValidationScript( ann1 )