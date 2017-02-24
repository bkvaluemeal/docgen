Types
=====

Object types for documentation generation

This module defines various containers for organizing the parts of a Python
package.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### Class(object)

A class

**Args:**

| Name | Type |    Description     |
|------|------|--------------------|
| obj  | Type | The object to wrap |


### Function(object)

A function

**Args:**

|  Name  |   Type   |            Description            |
|--------|----------|-----------------------------------|
| func   | Function | The function to wrap              |
| is_top | Bool     | Is this function in the top level |


### Module(object)

A module

**Args:**

| Name |  Type  |        Description         |
|------|--------|----------------------------|
| mod  | Module | The module to wrap         |
| pkg  | String | The location of the module |

#### save()

Saves the generated documentation

**Returns:**

|  Type  |                  Description                   |
|--------|------------------------------------------------|
| String | A string containing the location of the module |


### Package(object)

A package

**Args:**

| Name |  Type  |            Description            |
|------|--------|-----------------------------------|
| pkg  | String | The name of the package to import |

#### save()

Recursively saves the generated documentation

**Returns:**

| Type  |         Description          |
|-------|------------------------------|
| Tuple | A tuple of the modules saved |
