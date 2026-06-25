================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Baroness Gösta von dem Bussche-Haddenhausen (German: Freiin Gösta Julie Adelheid Marion Marie von dem Bussche-Haddenhausen; 26 January 1902 – 13 June 1996) was a German noblewoman and the mother of Prince Claus of the Netherlands.
Life in Germany

Gösta was born at Döbeln, Kingdom of Saxony, German Empire (now Saxony, Germany), the second child and daughter of Baron George von dem Bussche-Haddenhausen (1869–1923), and his wife, Baroness Gabriele von dem Bussche-Ippenburg (1877–1973).
Her father belonged to the Bussche-Haddenhausen branch of the Bussche family, and her mother belonged to the Bussche-Ippenburg branch.
Both of Gösta's parents were descended from Clamor von dem Bussche (1532–1573).
Gösta's mother was the heir of Dötzingen Estate near Hitzacker, which her maternal grandfather had inherited from the Counts von Oeynhausen after 1918.
Gösta's father was an officer in the Royal Saxon Army.
Dötzingen Estate later passed on to Gösta's brother Baron Julius von dem Bussche-Haddenhausen (1906–1977).
After Gösta's return from Africa and her husband's death in 1963, she spent the rest of her life in Dötzingen.
Gösta died at the age of 94 in Hitzacker, Germany.
Marriage

Gösta married Claus Felix von Amsberg (1890–1953), son of Wilhelm von Amsberg and Elise von Vieregge, on 4 September 1924 at Hitzacker.
Together, Gösta and Claus Felix had six daughters and one son:


Life in Africa

Gösta's husband Claus Felix had returned from the Tanganyika Territory (now Tanzania), a German colony, during World War I to become the manager of Dötzingen Estate in 1917.
Shortly after, the estate passed on to the Bussche family.
In 1924, Gösta and Claus Felix married, and in 1926, their son Claus was born at Dötzingen.
Claus Felix was the manager of a German-British tea and sisal plantation.
Claus was sent back to a German boarding school in 1933, but he returned to Africa in 1936.
In 1938, Gösta returned to Germany, and Claus was sent to a boarding school in Misdroy before being drafted by the army.
Gösta's husband returned to Germany in 1947.
Family relations

Gösta was a second cousin of Dorothea von Salviati (wife of Wilhelm, German Crown Prince's eldest son Prince Wilhelm of Prussia), both being great-granddaughters of Heinrich von Salviati and Caroline Rahlenbeck.
Gösta's younger and only brother Julius (1906–1977) was married to Anna-Elisabeth von Pfuel (1909–2005).
Gösta's family's home, Dötzingen Castle in Lower Saxony, had passed to her maternal grandfather, Eberhard Friedrich Gustav von dem Bussche-Ippenburg, from the Counts von Oeynhausen.
At a dinner party hosted by a distant cousin, the Count von Oeynhausen-Sierstorpff in Bad Driburg, on New Year's Eve 1962, Gösta's son Claus met then-Princess Beatrix of the Netherlands for the first time.
Beatrix, like Gösta and Claus, was a cousin of the Counts von Oeynhausen: Beatrix's paternal grandmother Armgard von Cramm was a daughter of Baron Aschwin of Sierstorpff-Cramm (1846–1909) and his wife, Baroness Hedwig von Sierstorpff-Driburg (1848–1900).
Armgard had first been married to Count Bodo von Oeynhausen before marrying Prince Bernhard of Lippe-Biesterfeld (1872–1934), Beatrix's paternal grandfather.
Additionally, Armgard's elder sister Baroness Hedwig von Sierstorpff-Cramm (1874–1907) was the heir to her mother's family's Driburg Estate.
Hedwig also married a Count von Oeynhausen, Wilhelm Karl Ludwig Kuno Graf von Oeynhausen-Sierstorpff (1860–1922), whose descendants still own the Driburg Estate.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (941f437d-8d34-444c-8e6b-46af57277ac2)
 Call ID: 941f437d-8d34-444c-8e6b-46af57277ac2
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    type: :Woman
  AssignClass (9c3faf75-ec20-45da-9f7d-77f1eefdd96e)
 Call ID: 9c3faf75-ec20-45da-9f7d-77f1eefdd96e
  Args:
    type: :Man
    source: George_von_dem_Bussche-Haddenhausen
  AssignClass (883ed5e1-7b6b-444d-8d3e-25b12a176f56)
 Call ID: 883ed5e1-7b6b-444d-8d3e-25b12a176f56
  Args:
    type: :Woman
    source: Gabriele_von_dem_Bussche-Ippenburg
  AssignClass (50320d2a-0f23-41d8-9dcc-ef0c083141ec)
 Call ID: 50320d2a-0f23-41d8-9dcc-ef0c083141ec
  Args:
    source: Clamor_von_dem_Bussche
    type: :Man
  AssignClass (b26297e6-ea28-4ba2-b1a7-2725d2e0e2d0)
 Call ID: b26297e6-ea28-4ba2-b1a7-2725d2e0e2d0
  Args:
    source: Julius_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (ba4d984d-68f8-4d95-be40-f7a85e0474db)
 Call ID: ba4d984d-68f8-4d95-be40-f7a85e0474db
  Args:
    type: :Man
    source: Claus_Felix_von_Amsberg
  AssignClass (cb3f5f3a-e66b-48c0-ac53-cc172dba82bd)
 Call ID: cb3f5f3a-e66b-48c0-ac53-cc172dba82bd
  Args:
    source: Wilhelm_von_Amsberg
    type: :Man
  AssignClass (785d9fac-a5c4-4a3f-a9e3-ab3852d96b18)
 Call ID: 785d9fac-a5c4-4a3f-a9e3-ab3852d96b18
  Args:
    type: :Woman
    source: Elise_von_Vieregge
  AssignClass (57f58bbf-4ce7-437d-8260-f37455fb2812)
 Call ID: 57f58bbf-4ce7-437d-8260-f37455fb2812
  Args:
    source: Claus_von_Amsberg
    type: :Man
  AddLiteral (91c12c7a-d16c-4599-9ad6-c42f13601693)
 Call ID: 91c12c7a-d16c-4599-9ad6-c42f13601693
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Gösta_von_dem_Bussche-Haddenhausen
    literal_value: 1902
  AddLiteral (10a8d080-9add-4819-9d22-2230091c0362)
 Call ID: 10a8d080-9add-4819-9d22-2230091c0362
  Args:
    literal_value: 1996
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (647dcdbc-6c5b-40b5-b053-249ed5e97585)
 Call ID: 647dcdbc-6c5b-40b5-b053-249ed5e97585
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1869
    source: George_von_dem_Bussche-Haddenhausen
  AddLiteral (6fbdc3c2-542a-4f86-9a06-78c0a4c06866)
 Call ID: 6fbdc3c2-542a-4f86-9a06-78c0a4c06866
  Args:
    literal_value: 1923
    source: George_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (af683df1-36a1-4e5d-8818-f264d086b755)
 Call ID: af683df1-36a1-4e5d-8818-f264d086b755
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    literal_value: 1877
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (b3c43bbd-f34c-416b-90d0-3a2afce1b13c)
 Call ID: b3c43bbd-f34c-416b-90d0-3a2afce1b13c
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    literal_value: 1973
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (60c680be-1327-490d-bd4f-6676f2b0aa35)
 Call ID: 60c680be-1327-490d-bd4f-6676f2b0aa35
  Args:
    source: Clamor_von_dem_Bussche
    literal_value: 1532
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (0d289016-3f86-45fd-b8da-7d61743686eb)
 Call ID: 0d289016-3f86-45fd-b8da-7d61743686eb
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Clamor_von_dem_Bussche
    literal_value: 1573
  AddLiteral (46b27d81-4dd5-4607-81fb-f3c1de99df91)
 Call ID: 46b27d81-4dd5-4607-81fb-f3c1de99df91
  Args:
    literal_value: 1906
    source: Julius_von_dem_Bussche-Haddenhausen
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (3b809a32-90bb-45a2-ab52-52af627fba8d)
 Call ID: 3b809a32-90bb-45a2-ab52-52af627fba8d
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1977
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (40856825-a00d-49b1-a237-122625da4d86)
 Call ID: 40856825-a00d-49b1-a237-122625da4d86
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Claus_Felix_von_Amsberg
    literal_value: 1890
  AddLiteral (b9197412-c421-4705-9ce5-ede0234090b0)
 Call ID: b9197412-c421-4705-9ce5-ede0234090b0
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1953
    source: Claus_Felix_von_Amsberg
  AddLiteral (b95befe4-9bda-4726-b49b-946b3a33d5ce)
 Call ID: b95befe4-9bda-4726-b49b-946b3a33d5ce
  Args:
    source: Claus_von_Amsberg
    literal_value: 1926
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (6b6fab5c-9a6f-43d9-ac86-4903c0bdf2ea)
 Call ID: 6b6fab5c-9a6f-43d9-ac86-4903c0bdf2ea
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    target: George_von_dem_Bussche-Haddenhausen
    relation: :hasFather
  AddTriple (93131ee5-9ae7-4dfd-9150-2c91f73555d4)
 Call ID: 93131ee5-9ae7-4dfd-9150-2c91f73555d4
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    target: Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasMother
  AddTriple (57b93721-0e44-4cca-9f4e-43fbbf6cba2b)
 Call ID: 57b93721-0e44-4cca-9f4e-43fbbf6cba2b
  Args:
    relation: :hasFather
    target: George_von_dem_Bussche-Haddenhausen
    source: Julius_von_dem_Bussche-Haddenhausen
  AddTriple (31540040-bab3-4fad-9a1f-c0185c9f83b3)
 Call ID: 31540040-bab3-4fad-9a1f-c0185c9f83b3
  Args:
    target: Gabriele_von_dem_Bussche-Ippenburg
    source: Julius_von_dem_Bussche-Haddenhausen
    relation: :hasMother
  AddTriple (4e173d31-1cb2-4550-9b4d-edb7769b2339)
 Call ID: 4e173d31-1cb2-4550-9b4d-edb7769b2339
  Args:
    relation: :hasFather
    target: Claus_Felix_von_Amsberg
    source: Claus_von_Amsberg
  AddTriple (77ec257e-5d34-4ea6-a253-2308c1586b84)
 Call ID: 77ec257e-5d34-4ea6-a253-2308c1586b84
  Args:
    relation: :hasMother
    source: Claus_von_Amsberg
    target: Gösta_von_dem_Bussche-Haddenhausen
  AddTriple (b45414c7-2916-419d-ab59-6ef0611b4c2a)
 Call ID: b45414c7-2916-419d-ab59-6ef0611b4c2a
  Args:
    relation: :hasFather
    source: Claus_Felix_von_Amsberg
    target: Wilhelm_von_Amsberg
  AddTriple (18ed55a9-1745-4de4-ac36-c89c0bee1a05)
 Call ID: 18ed55a9-1745-4de4-ac36-c89c0bee1a05
  Args:
    target: Elise_von_Vieregge
    source: Claus_Felix_von_Amsberg
    relation: :hasMother
  AddLiteral (ce793e04-8a6c-492e-ad82-2cf50509fef4)
 Call ID: ce793e04-8a6c-492e-ad82-2cf50509fef4
  Args:
    literal_value: 1924
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasMarriageYear
    literal_type: xsd:integer
  Finish (68d96855-6de4-4704-8307-91e5f93b791a)
 Call ID: 68d96855-6de4-4704-8307-91e5f93b791a
  Args: