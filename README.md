# Coding Challenge

_Warning: This repository was created for coding challenge only._

There are 2 main tasks here:
 1. `Testing a Struct interface:` Writing a comprehensive set of unit tests to test all the behaviors defined by the interface specification.
 
 2. `Data Store Library`: Designing and implementing a library that can be used to store and retrieve arbitrary data in multiple formats & destinations.
  This library can be used by 3rd party developers, and it exposes a simple and structured
  API.
  A record is defined as a simple data structure where every key maps to a primitive value
  (fields values cannot be objects, arrays etc).
  Given this definition of a record, the library supports the following operations:
   * Record inserts & batch inserts
   * Record query/retrieval
   * Query filters (equality operations only), limit & offset
   * Update and delete operations
   
