# Role
You are a Semantic Web Expert and Data Quality Consultant. Your task is to analyze technical SHACL (Shapes Constraint Language) validation errors and translate them into a clear, actionable correction plan.

# Context
I am constructing a Knowledge Graph based on a provided ontology. Some extracted triples have failed validation. You need to explain these failures simply so they can be corrected in the next step.

# Task
For each violation in the `{violations}` report:
1. **Identify the Subject:** The specific entity (focus node) triggered the error.
2. **Identify the Problem:** The specific property or relation that is missing, extra, or incorrectly formatted.
3. **Explain the Logic:** Why did this fail based on the constraint? (e.g., "This property is not allowed for this class," or "This value must be a URI, but a string was provided").
4. **Define the Fix:** Provide a precise instruction on how to change the triple to satisfy the ontology.

# Raw SHACL Violations
### entry_1
Text: Origins and Early Ascent
The origins of the House of Habsburg are traced back to the 10th century, specifically to Guntram the Rich, a count in Breisgau. His grandson, Radbot, Count of Klettgau, is credited with building the Habichtsburg (Hawk’s Castle) in the Swiss Canton of Aargau around 1020, from which the family name is derived. Radbot’s marriage to Ida of Lorraine established an early link to the Carolingian bloodline, a crucial bit of "ancestral proof" for their later claims to the Holy Roman Empire.

The transition from local counts to European power players began with Rudolf I of Germany (1218–1291). He was the son of Albert IV, Count of Habsburg, and Hedwig of Kyburg. Upon his election as King of the Romans, Rudolf secured the Duchies of Austria and Styria for his sons, Albert I and Rudolf II, effectively moving the family’s center of power from Switzerland to Vienna. Albert I’s subsequent marriage to Elisabeth of Carinthia produced a staggering fifteen children, ensuring the biological survival of the line but creating a complex web of cadet branches.

The Great Dynastic Split
The most significant expansion occurred under Maximilian I, who used marriage as a tool of statecraft. His own marriage to Mary of Burgundy brought the Low Countries into the Habsburg fold. Their son, Philip the Handsome, married Joanna of Castile (known as Joanna the Mad), the daughter of the "Catholic Monarchs" Ferdinand and Isabella of Spain. This single union merged the Austrian and Spanish legacies.

This resulted in Charles V (Holy Roman Emperor and King of Spain), who arguably held the most complex set of relations in history. Charles V was the grandson of four monarchs: Maximilian I and Mary of Burgundy (paternal), and Ferdinand II of Aragon and Isabella I of Castile (maternal). To manage his vast "Empire on which the sun never sets," Charles eventually abdicated, splitting the house into two distinct but deeply intertwined branches:

The Spanish Habsburgs: Led by his son, Philip II.

The Austrian Habsburgs: Led by his brother, Ferdinand I.

The Inbreeding Spiral
To keep power within the family, the two branches began a centuries-long pattern of intermarriage. Philip II of Spain, for instance, married four times. His second wife, Mary I of England, was his first cousin once removed. His fourth wife, Anna of Austria, was his own niece (the daughter of his sister Mary and his cousin Maximilian II).

This culminated in Charles II of Spain, the "bewitched" king. Genetically, Charles II was more inbred than the offspring of two siblings because his ancestors had married their own nieces and cousins for generations. His father, Philip IV, was the uncle of his mother, Mariana of Austria. Furthermore, Mariana was the daughter of Empress Maria Anna, who was Philip IV’s sister. This means Charles II’s grandmother was also his aunt.
Violations summary:
- Total violations: 13
- Expected correction items: roughly one triple per violation item below (you may satisfy multiple items with one triple only if it is explicitly valid to do so).
Correction items:

Target triple index -1 (no matching existing triple):
- You likely need to ADD new triple(s).

  [1] Correction item
  - focus node: entry_1__Ida_of_Lorraine
  - property path: hasSex
  - ontology definition of the property:

    fhkb:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Sex .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Ida_of_Lorraine->fhkb:hasSex
  - source shape:

    fhkb:Woman-hasSex a sh:PropertyShape ;
    dash:hasValueWithClass fhkb:Female ;
    sh:class fhkb:Sex ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasSex .


  [2] Correction item
  - focus node: entry_1__Radbot
  - property path: hasFather
  - ontology definition of the property:

    fhkb:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isFatherOf .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Radbot->fhkb:hasFather
  - source shape:

    fhkb:Person-hasFather a sh:PropertyShape ;
    sh:class fhkb:Man ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasFather .


  [3] Correction item
  - focus node: entry_1__Guntram_the_Rich
  - property path: hasFather
  - ontology definition of the property:

    fhkb:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isFatherOf .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Guntram_the_Rich->fhkb:hasFather
  - source shape:

    fhkb:Person-hasFather a sh:PropertyShape ;
    sh:class fhkb:Man ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasFather .


  [4] Correction item
  - focus node: entry_1__Radbot
  - property path: hasSex
  - ontology definition of the property:

    fhkb:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Sex .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Radbot->fhkb:hasSex
  - source shape:

    fhkb:Person-hasSex a sh:PropertyShape ;
    sh:class fhkb:Sex ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasSex .


  [5] Correction item
  - focus node: entry_1__Guntram_the_Rich
  - property path: hasSex
  - ontology definition of the property:

    fhkb:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Sex .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Guntram_the_Rich->fhkb:hasSex
  - source shape:

    fhkb:Person-hasSex a sh:PropertyShape ;
    sh:class fhkb:Sex ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasSex .


  [6] Correction item
  - focus node: entry_1__Radbot
  - property path: hasMother
  - ontology definition of the property:

    fhkb:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isMotherOf .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Radbot->fhkb:hasMother
  - source shape:

    fhkb:Person-hasMother a sh:PropertyShape ;
    sh:class fhkb:Woman ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasMother .


  [7] Correction item
  - focus node: entry_1__Guntram_the_Rich
  - property path: hasMother
  - ontology definition of the property:

    fhkb:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isMotherOf .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Guntram_the_Rich->fhkb:hasMother
  - source shape:

    fhkb:Person-hasMother a sh:PropertyShape ;
    sh:class fhkb:Woman ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasMother .


Target triple index 0 (existing triple to edit):
- Current triple: (Guntram_the_Rich, hasRelation, House_of_Habsburg)
- Current schema types: (Person, DomainEntity)
- Ontology definitions of the types:
  - Subject type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

  - Object type DomainEntity:

    fhkb:DomainEntity a owl:Class .


  [8] Correction item
  - focus node: entry_1__Guntram_the_Rich
  - property path: hasRelation
  - ontology definition of the property:

    fhkb:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person .

  - value: entry_1__House_of_Habsburg
  - constraint: http://www.w3.org/ns/shacl#ClassConstraintComponent
  - violation: Value does not have class fhkb:Person
  - source shape:

    fhkb:Person-hasRelation a sh:PropertyShape ;
    sh:class fhkb:Person ;
    sh:path fhkb:hasRelation .


Target triple index 1 (existing triple to edit):
- Current triple: (Radbot, hasAncestor, Guntram_the_Rich)
- Current schema types: (Person, Person)
- Ontology definitions of the types:
  - Subject type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

  - Object type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .


  [9] Correction item
  - focus node: entry_1__Radbot
  - property path: hasAncestor
  - ontology definition of the property:

    fhkb:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:subPropertyOf fhkb:hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf fhkb:isAncestorOf .

  - value: entry_1__Guntram_the_Rich
  - constraint: http://www.w3.org/ns/shacl#ClosedConstraintComponent
  - violation: Node ex:entry_1__Radbot is closed. It cannot have value: ex:entry_1__Guntram_the_Rich
  - source shape:

    fhkb:Person a rdfs:Class,
        sh:NodeShape ;
    sh:closed true ;
    sh:ignoredProperties ( rdf:type ) ;
    sh:property fhkb:Person-hasFather,
        fhkb:Person-hasMother,
        fhkb:Person-hasParent,
        fhkb:Person-hasRelation,
        fhkb:Person-hasSex .


Target triple index 2 (existing triple to edit):
- Current triple: (Radbot, hasRelation, Habichtsburg)
- Current schema types: (Person, DomainEntity)
- Ontology definitions of the types:
  - Subject type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

  - Object type DomainEntity:

    fhkb:DomainEntity a owl:Class .


  [10] Correction item
  - focus node: entry_1__Radbot
  - property path: hasRelation
  - ontology definition of the property:

    fhkb:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person .

  - value: entry_1__Habichtsburg
  - constraint: http://www.w3.org/ns/shacl#ClassConstraintComponent
  - violation: Value does not have class fhkb:Person
  - source shape:

    fhkb:Person-hasRelation a sh:PropertyShape ;
    sh:class fhkb:Person ;
    sh:path fhkb:hasRelation .


Target triple index 3 (existing triple to edit):
- Current triple: (Radbot, hasWife, Ida_of_Lorraine)
- Current schema types: (Person, Woman)
- Ontology definitions of the types:
  - Subject type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

  - Object type Woman:

    fhkb:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( fhkb:Person [ a owl:Restriction ;
                        owl:onProperty fhkb:hasSex ;
                        owl:someValuesFrom fhkb:Female ] ) ] .


  [11] Correction item
  - focus node: entry_1__Radbot
  - property path: hasWife
  - ontology definition of the property:

    fhkb:hasWife a owl:ObjectProperty ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasSpouse ;
    owl:inverseOf fhkb:isWifeOf ;
    owl:propertyChainAxiom ( fhkb:isMalePartnerIn fhkb:hasFemalePartner ) .

  - value: entry_1__Ida_of_Lorraine
  - constraint: http://www.w3.org/ns/shacl#ClosedConstraintComponent
  - violation: Node ex:entry_1__Radbot is closed. It cannot have value: ex:entry_1__Ida_of_Lorraine
  - source shape:

    fhkb:Person a rdfs:Class,
        sh:NodeShape ;
    sh:closed true ;
    sh:ignoredProperties ( rdf:type ) ;
    sh:property fhkb:Person-hasFather,
        fhkb:Person-hasMother,
        fhkb:Person-hasParent,
        fhkb:Person-hasRelation,
        fhkb:Person-hasSex .


Target triple index 4 (existing triple to edit):
- Current triple: (Ida_of_Lorraine, hasRelation, Carolingian_bloodline)
- Current schema types: (Woman, DomainEntity)
- Ontology definitions of the types:
  - Subject type Woman:

    fhkb:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( fhkb:Person [ a owl:Restriction ;
                        owl:onProperty fhkb:hasSex ;
                        owl:someValuesFrom fhkb:Female ] ) ] .

  - Object type DomainEntity:

    fhkb:DomainEntity a owl:Class .


  [12] Correction item
  - focus node: entry_1__Ida_of_Lorraine
  - property path: hasRelation
  - ontology definition of the property:

    fhkb:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person .

  - value: entry_1__Carolingian_bloodline
  - constraint: http://www.w3.org/ns/shacl#ClosedConstraintComponent
  - violation: Node ex:entry_1__Ida_of_Lorraine is closed. It cannot have value: ex:entry_1__Carolingian_bloodline
  - source shape:

    fhkb:Woman a rdfs:Class,
        sh:NodeShape ;
    rdfs:subClassOf [ ] ;
    owl:intersectionOf [ ] ;
    sh:closed true ;
    sh:ignoredProperties ( rdf:type ) ;
    sh:property fhkb:Woman-hasSex,
        fhkb:Woman-isSisterOf .


Target triple index 5 (existing triple to edit):
- Current triple: (Radbot, hasRelation, Carolingian_bloodline)
- Current schema types: (Person, DomainEntity)
- Ontology definitions of the types:
  - Subject type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

  - Object type DomainEntity:

    fhkb:DomainEntity a owl:Class .


  [13] Correction item
  - focus node: entry_1__Radbot
  - property path: hasRelation
  - ontology definition of the property:

    fhkb:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person .

  - value: entry_1__Carolingian_bloodline
  - constraint: http://www.w3.org/ns/shacl#ClassConstraintComponent
  - violation: Value does not have class fhkb:Person
  - source shape:

    fhkb:Person-hasRelation a sh:PropertyShape ;
    sh:class fhkb:Person ;
    sh:path fhkb:hasRelation .



# Simplified Output Format
| Violation Number | Triple Index | What's Wrong? | How to Fix It |
| :--- | :--- | :--- | :--- |
| [ID] | [Triple Index] | [Simple Logic Explanation] | [Specific Technical Instruction] |

---
**Constraint for LLM:** Focus on the structural and logical requirements of the ontology. Use local names (e.g., `hasFather`) instead of full URIs in the "What's Wrong" column to ensure clarity.