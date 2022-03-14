import json

from apache_atlas.client.base_client import AtlasClient
from apache_atlas.model.instance import AtlasEntityWithExtInfo
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
        # return client.entity.update_entity(entity)


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
]

# Create Typedefs
for path in json_type_defs:
    create_type_defs(path)

# Create Entities
for path in json_entity_defs:
    create_entities(path)

# Delete
# for path in json_type_defs:
#     delete_type_defs(path)
