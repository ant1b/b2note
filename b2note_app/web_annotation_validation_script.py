import re, os, datetime, json, glob, errno, sys
from jsonschema import validate


def readyQuerySetValuesForDumpAsJSONLD( o_in ):
    """
      Function: readyQuerySetValuesForDumpAsJSONLD
      --------------------------------------------

        Recursively drops embedded custom model class objects and model
         class field names beginning with "jsonld_whatever" to "@whatever",
         while avoiding returning fields with no content and making
         datetimes to xsd:datetime strings.

        input:
            o_in (object): In nesting order, Django queryset values
                list then tuple or list or set or dict or datetime or
                out-of-scope object.

        output:
            o_out: None (execution failed) or list of native python
                objects, where each out-of-scope object was replaced
                by its "string-ified" avatar, designed for subsequent
                JSON-ification.
    """

    o_out = None

    try:
        if type(o_in) is tuple:
            o_out = ()
            for item in o_in:
                if item and readyQuerySetValuesForDumpAsJSONLD( item ):
                    o_out += ( readyQuerySetValuesForDumpAsJSONLD( item ), )
        elif isinstance(o_in, (list, set)):
            o_out = []
            if len(o_in)==1:
               if o_in[0]:
                   o_out = o_in[0]
            if o_out == []:
                for item in o_in:
                    if item and readyQuerySetValuesForDumpAsJSONLD( item ):
                        o_out.append( readyQuerySetValuesForDumpAsJSONLD( item ) )
        elif type(o_in) is dict:
            o_out = {}
            for k in o_in.keys():
                if o_in[k] and readyQuerySetValuesForDumpAsJSONLD( o_in[k] ) and k != "id":
                    newkey = k
                    m = re.match(r'^jsonld_(.*)', k)
                    if m:
                        newkey = "@{0}".format(m.group(1))
                    o_out[newkey] = readyQuerySetValuesForDumpAsJSONLD( o_in[k] )
        elif isinstance(o_in, datetime.datetime) or isinstance(o_in, datetime.datetime):
            o_out = o_in.isoformat()
        elif o_in and o_in != "None" and not re.match(r'^<class (.*)>', o_in):
            o_out = unicode(str(o_in))
        #if len(o_out) <= 0: o_out = Non
    except:
        o_out = None
        pass

    return o_out


def web_annotation_valid( ann_json=None ):

    try:

        passesalltests = True

        #http://askubuntu.com/questions/352198/reading-all-files-from-a-directory

        #path = os.path.join(global_settings.STATIC_PATH, 'files/web_annotation/tests/*.json')
        path = os.getcwd()
        path = path + '/static/files/web-annotation/tests/*.json'

        files = glob.glob(path)

        for name in files:  # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
            try:
                with open(name) as f:  # No need to specify 'r': this is the default.

                    try:

                        schema = f.read()

                        try:
                            schema = json.loads( schema )
                        except:
                            print "Could not load jsonschema."
                            break

                        try:
                            validate( ann_json, schema )
                        except:
                            print "JSON does not validate against web annotation validator."
                            return False

                    except:
                        print "Validation schema could not be loaded:", name
                        return False

            except IOError as exc:
                passesalltests = False
                if exc.errno != errno.EISDIR:  # Do not fail if a directory is found, just ignore it.
                    raise  # Propagate other kinds of IOError.

        if passesalltests: return True

    except:

        print "web_annotation_valid failed."
        return False

    return False



def webAnnotationJsonValidationScript( ann_json=None ):

    try:

        if ann_json and isinstance(ann_json, (str, unicode)) and len(ann_json)>0:

            try:

                json_o = json.loads(ann_json)

                json_o = readyQuerySetValuesForDumpAsJSONLD(json_o)

                if web_annotation_valid( json_o ): return True

            except:

                print "Provided object cannot be loaded as json in python."
                return False

        else:

            print "Provided object is not string or too short for being valid json."
            return False

    except:

        pass
        return False

    print "Provided object was not found to pass simple web annotation validation."
    return False


def jsonldAnnotationListValid( jsonld=None ):

    try:

        allAnnotationsValid = True

        ann_dict = json.loads( jsonld )

        if ann_dict and isinstance(ann_dict, dict):

            if "@context" in ann_dict.keys() and "@graph" in ann_dict.keys():

                if ann_dict["@context"] and isinstance(ann_dict["@context"], (str, unicode, list)):

                    ann_list = ann_dict["@graph"]

                    if ann_list and isinstance(ann_list, (list, set)):

                        for ann in ann_list:

                            if ann and isinstance(ann, dict):

                                if not webAnnotationJsonValidationScript( json.dumps(ann) ):

                                    print "One annotation could not pass validators:", json.dumps(ann)
                                    return False

                            else:

                                print "One member of the list is not a dictionary."
                                return False

                        print "Valid JSON-LD containing valid annotations."
                        return True

                    else:

                        print "Provided object '@graph' field does not contain a valid list."
                        return False

                else:

                    print "Provided object is not a valid list."
                    return False

            else:

                print "Provided dictionary object is missing field '@context' or '@graph'."
                return False

        else:

            print "Provided object is not a valid container of web annotations."
            return False

    except:

        print "jsonldWebAnnotationListvalid function failed."
        return False

    return False



ann1 = '''{
      "body": [
          {
            "type": [
              "TextualBody"
            ],
            "@id": "http://purl.obolibrary.org/obo/GAZ_00448034",
            "modified": "2016-08-31T11:17:09.705000",
            "value": "Loch Tralaig",
            "created": "2016-08-31T09:17:09.627000"
          }
      ],
      "target": [
          {
            "@id": "https://b2share.eudat.eu/record/30",
            "modified": "2016-08-31T11:17:09.706000",
            "language": ["en"],
            "created": "2016-08-31T09:17:09.627000"
          }
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
          {
            "type": [
              "TextualBody"
            ],
            "@id": "http://purl.uniprot.org/uniprot/P30249",
            "modified": "2016-08-31T13:09:37.401000",
            "value": "Locustatachykinin-3",
            "created": "2016-08-31T11:09:37.394000"
          }
      ],
      "target": [
          {
            "@id": "https://b2share.eudat.eu/record/30",
            "modified": "2016-08-31T13:09:37.401000",
            "language": ["en"],
            "created": "2016-08-31T11:09:37.394000"
          }
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
    }'''


test_jsonld = '''{
    "@context": "http://www.w3.org/ns/anno.jsonld",
    "@graph": [''' + ann2 + ''',''' + ann1 + ''']
}'''

jsonldAnnotationListValid( test_jsonld )