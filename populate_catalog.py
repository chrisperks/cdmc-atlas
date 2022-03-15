import json

from apache_atlas.client.base_client import AtlasClient
from apache_atlas.model.instance import AtlasEntityWithExtInfo
from apache_atlas.model.glossary import (
    AtlasGlossary,
    AtlasGlossaryHeader,
    AtlasGlossaryTerm,
)
from apache_atlas.model.typedef import AtlasTypesDef, AtlasAttributeDef
from apache_atlas.utils import type_coerce

client = AtlasClient("http://localhost:21000", ("admin", "admin"))


def load_type_defs_from_json(json_path, skip_existing=True):
    """
    Load defs from JSON
    """
    with open(json_path, encoding="utf-8") as f:
        type_def = type_coerce(json.load(f), AtlasTypesDef)

        types_to_create = AtlasTypesDef()

        types_to_create.enumDefs = []
        types_to_create.structDefs = []
        types_to_create.classificationDefs = []
        types_to_create.entityDefs = []
        types_to_create.relationshipDefs = []
        types_to_create.businessMetadataDefs = []

        for enum_def in type_def.enumDefs:
            if skip_existing and client.typedef.type_with_name_exists(enum_def.name):
                print("Type with name %s already exists. Skipping.", enum_def.name)
            else:
                types_to_create.enumDefs.append(enum_def)

        for struct_def in type_def.structDefs:
            if skip_existing and client.typedef.type_with_name_exists(struct_def.name):
                print("Type with name %s already exists. Skipping.", struct_def.name)
            else:
                types_to_create.structDefs.append(struct_def)

        for classification_def in type_def.classificationDefs:
            if skip_existing and client.typedef.type_with_name_exists(
                classification_def.name
            ):
                print(
                    "Type with name %s already exists. Skipping.",
                    classification_def.name,
                )
            else:
                types_to_create.classificationDefs.append(classification_def)

        for entity_def in type_def.entityDefs:
            entity_def.attributeDefs.append(AtlasAttributeDef({}))
            if skip_existing and client.typedef.type_with_name_exists(entity_def.name):
                print("Type with name %s already exists. Skipping.", entity_def.name)
            else:
                types_to_create.entityDefs.append(entity_def)

        for relationship_def in type_def.relationshipDefs:
            if skip_existing and client.typedef.type_with_name_exists(
                relationship_def.name
            ):
                print(
                    "Type with name %s already exists. Skipping.", relationship_def.name
                )
            else:
                types_to_create.relationshipDefs.append(relationship_def)

        for business_metadata_def in type_def.businessMetadataDefs:
            if skip_existing and client.typedef.type_with_name_exists(
                business_metadata_def.name
            ):
                print(
                    "Type with name %s already exists. Skipping.",
                    business_metadata_def.name,
                )
            else:
                types_to_create.businessMetadataDefs.append(business_metadata_def)
        return types_to_create


def create_type_defs(json_path):
    """
    Create the typedefs
    """
    types_to_create = load_type_defs_from_json(json_path)
    return client.typedef.create_atlas_typedefs(types_to_create)


def delete_type_defs(json_path):
    """
    Delete the typedefs
    """

    type_defs = load_type_defs_from_json(json_path, False)

    names_to_delete = []
    names_to_delete.extend(
        [type_def["name"] for type_def in type_defs.relationshipDefs]
    )
    names_to_delete.extend([type_def["name"] for type_def in type_defs.enumDefs])
    names_to_delete.extend([type_def["name"] for type_def in type_defs.structDefs])
    names_to_delete.extend(
        [type_def["name"] for type_def in type_defs.classificationDefs]
    )
    names_to_delete.extend(
        [type_def["name"] for type_def in type_defs.businessMetadataDefs]
    )
    names_to_delete.extend([type_def["name"] for type_def in type_defs.entityDefs])

    for typedef_name in names_to_delete:
        print("deleting " + typedef_name)
        client.typedef.delete_type_by_name(typedef_name)


def create_entities(json_path):
    """
    Create entities
    """
    with open(json_path, encoding="utf-8") as f:
        entity = type_coerce(json.load(f), AtlasEntityWithExtInfo)
        print("Creating or updating " + entity.entity.attributes["name"])
        return client.entity.create_entity(entity)


def create_glossary(json_path):
    """
    Create glossary
    """
    with open(json_path, encoding="utf-8") as f:

        raw_json = json.load(f)
        glossary = type_coerce(raw_json, AtlasGlossary)
        terms = [type_coerce(x, AtlasGlossaryTerm) for x in raw_json["terms"]]

        for existing_glossary in client.glossary.get_all_glossaries():
            if existing_glossary["name"] == glossary.name:
                client.glossary.delete_glossary_by_guid(existing_glossary["guid"])

        print("Creating or updating " + glossary.name)
        new_glossary = client.glossary.create_glossary(glossary)

        shared_glossary_header = AtlasGlossaryHeader()
        shared_glossary_header.glossaryGuid = new_glossary.guid
        shared_glossary_header.displayText = glossary.name

        for term in terms:
            term.anchor = shared_glossary_header

        client.glossary.create_glossary_terms(terms)


json_type_defs = [
    "models/2000_SQLDB_typedefs.json",
    "models/3000_AWS_S3_typedefs.json",
    "models/3500_Azure_ADLS_typedefs.json",
]

json_entity_defs = [
    "models/2100_SQLDB_entitydefs_ASMSQL001@sqldb.json",
    "models/2101_SQLDB_entitydefs_accounts_db@sqldb.json",
    "models/2110_SQLDB_entitydefs_accounts_account_table@sqldb.json",
    "models/2111_SQLDB_entitydefs_accounts_address_table@sqldb.json",
    "models/2112_SQLDB_entitydefs_accounts_contact_table@sqldb.json",
    "models/2113_SQLDB_entitydefs_accounts_socialprofile_table@sqldb.json",
    "models/2150_SQLDB_entitydefs_communications_db@sqldb.json",
    "models/2151_SQLDB_entitydefs_communications_article_table@sqldb.json",
    "models/3101_AWS_entitydefs_bucket_email@aws.json",
    "models/3102_AWS_entitydefs_bucket_fax@aws.json",
    "models/3103_AWS_entitydefs_bucket_feedback@aws.json",
    "models/3104_AWS_entitydefs_bucket_note@aws.json",
    "models/3105_AWS_entitydefs_bucket_letter@aws.json",
    "models/3106_AWS_entitydefs_bucket_phonecall@aws.json",
    "models/3107_AWS_entitydefs_bucket_socialactivity@aws.json",
    "models/3110_AWS_entitydefs_bucket_communications_merged@aws.json",
    "models/3111_AWS_entitydefs_bucket_communications_cleaned@aws.json",
    "models/3200_AWS_entitydefs_hourly_s3_comms_merge@aws.json",
    "models/3201_AWS_entitydefs_hourly_s3_comms_clean@aws.json",
]

json_glossary_defs = ["models/4000_Glossary_EDM_DCAM.json"]

# Create Typedefs
for path in json_type_defs:
    create_type_defs(path)

# Create Entities
for path in json_entity_defs:
    create_entities(path)

# Create Glossaries
# for path in json_glossary_defs:
#     create_glossary(path)
