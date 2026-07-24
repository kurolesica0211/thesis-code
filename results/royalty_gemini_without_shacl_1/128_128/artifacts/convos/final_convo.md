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
  AssignClass (b8e8af8c-9308-42b5-9dbe-0f44d372dcbf)
 Call ID: b8e8af8c-9308-42b5-9dbe-0f44d372dcbf
  Args:
    type: :Woman
    source: :Gosta_von_dem_Bussche-Haddenhausen
  AssignClass (f5775479-db99-4247-8eaa-66c08fa54d78)
 Call ID: f5775479-db99-4247-8eaa-66c08fa54d78
  Args:
    source: :George_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (a5677018-e05d-4ed8-8c5b-198dade6a4cb)
 Call ID: a5677018-e05d-4ed8-8c5b-198dade6a4cb
  Args:
    source: :Gabriele_von_dem_Bussche-Ippenburg
    type: :Woman
  AssignClass (e4ee5325-a1d7-4b70-b3e0-0a52e1af8e4b)
 Call ID: e4ee5325-a1d7-4b70-b3e0-0a52e1af8e4b
  Args:
    source: :Claus_Felix_von_Amsberg
    type: :Man
  AssignClass (06fc545d-38c8-42a3-9c63-0d371e3ee11c)
 Call ID: 06fc545d-38c8-42a3-9c63-0d371e3ee11c
  Args:
    source: :Wilhelm_von_Amsberg
    type: :Man
  AssignClass (af68ef99-bc64-4a2b-a82a-7a0ea12017d4)
 Call ID: af68ef99-bc64-4a2b-a82a-7a0ea12017d4
  Args:
    type: :Woman
    source: :Elise_von_Vieregge
  AssignClass (3e721716-7fc2-4e33-b90f-a198321a07f0)
 Call ID: 3e721716-7fc2-4e33-b90f-a198321a07f0
  Args:
    type: :Man
    source: :Claus_von_Amsberg
  AssignClass (5d6482d1-8b53-4e00-b971-f9f96cdebcde)
 Call ID: 5d6482d1-8b53-4e00-b971-f9f96cdebcde
  Args:
    type: :Man
    source: :Julius_von_dem_Bussche-Haddenhausen
  AssignClass (2a745b8c-9791-46a4-81d2-54a003d8007e)
 Call ID: 2a745b8c-9791-46a4-81d2-54a003d8007e
  Args:
    type: :Woman
    source: :Anna-Elisabeth_von_Pfuel
  AddLiteral (0b5ee694-4d2a-444f-a0e6-d75c6d81be71)
 Call ID: 0b5ee694-4d2a-444f-a0e6-d75c6d81be71
  Args:
    literal_type: xsd:integer
    literal_value: 1902
    relation: :hasBirthYear
    source: :Gosta_von_dem_Bussche-Haddenhausen
  AddLiteral (a584008c-0da0-4aac-990a-fca14bc8dea9)
 Call ID: a584008c-0da0-4aac-990a-fca14bc8dea9
  Args:
    literal_value: 1996
    literal_type: xsd:integer
    source: :Gosta_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
  AddTriple (a0bc28d5-17b9-485e-b378-e7aaa9ba03ea)
 Call ID: a0bc28d5-17b9-485e-b378-e7aaa9ba03ea
  Args:
    relation: :hasFather
    source: :Gosta_von_dem_Bussche-Haddenhausen
    target: :George_von_dem_Bussche-Haddenhausen
  AddTriple (4ee295f8-1fca-4dfc-b619-d3f42dec82f0)
 Call ID: 4ee295f8-1fca-4dfc-b619-d3f42dec82f0
  Args:
    relation: :hasMother
    target: :Gabriele_von_dem_Bussche-Ippenburg
    source: :Gosta_von_dem_Bussche-Haddenhausen
  AddLiteral (cb5d98cb-b5ea-4dd1-8b90-8bde452a535e)
 Call ID: cb5d98cb-b5ea-4dd1-8b90-8bde452a535e
  Args:
    literal_type: xsd:integer
    literal_value: 1869
    relation: :hasBirthYear
    source: :George_von_dem_Bussche-Haddenhausen
  AddLiteral (78bf37bc-7a25-4bbb-9f8a-4988fd63df1d)
 Call ID: 78bf37bc-7a25-4bbb-9f8a-4988fd63df1d
  Args:
    literal_value: 1923
    literal_type: xsd:integer
    source: :George_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
  AddLiteral (33ad2e03-0c00-4c5f-9f46-9b1cfe6d045b)
 Call ID: 33ad2e03-0c00-4c5f-9f46-9b1cfe6d045b
  Args:
    relation: :hasBirthYear
    source: :Gabriele_von_dem_Bussche-Ippenburg
    literal_type: xsd:integer
    literal_value: 1877
  AddLiteral (9e59a840-01dd-4812-87ad-4f01284af642)
 Call ID: 9e59a840-01dd-4812-87ad-4f01284af642
  Args:
    literal_value: 1973
    literal_type: xsd:integer
    source: :Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasDeathYear
  AddTriple (3ee55378-62d2-43f0-86b3-10b2b4cd83f4)
 Call ID: 3ee55378-62d2-43f0-86b3-10b2b4cd83f4
  Args:
    relation: :hasFather
    source: :Claus_Felix_von_Amsberg
    target: :Wilhelm_von_Amsberg
  AddTriple (adde0b22-c61f-4d98-b370-93286c15e20b)
 Call ID: adde0b22-c61f-4d98-b370-93286c15e20b
  Args:
    relation: :hasMother
    source: :Claus_Felix_von_Amsberg
    target: :Elise_von_Vieregge
  AddLiteral (9489baaa-3e60-4d04-818d-72badb87e0a8)
 Call ID: 9489baaa-3e60-4d04-818d-72badb87e0a8
  Args:
    relation: :hasBirthYear
    source: :Claus_Felix_von_Amsberg
    literal_type: xsd:integer
    literal_value: 1890
  AddLiteral (89b7d0e6-8c97-4bec-808c-f41538e32663)
 Call ID: 89b7d0e6-8c97-4bec-808c-f41538e32663
  Args:
    source: :Claus_Felix_von_Amsberg
    relation: :hasDeathYear
    literal_value: 1953
    literal_type: xsd:integer
  AddLiteral (21f8ee2c-1877-436e-819b-f0ad0c0781dd)
 Call ID: 21f8ee2c-1877-436e-819b-f0ad0c0781dd
  Args:
    relation: :hasMarriageYear
    source: :Gosta_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
    literal_value: 1924
  AddTriple (4716ad84-743d-4970-b602-f8b5988629f0)
 Call ID: 4716ad84-743d-4970-b602-f8b5988629f0
  Args:
    source: :Claus_von_Amsberg
    target: :Claus_Felix_von_Amsberg
    relation: :hasFather
  AddTriple (b47e7320-028a-452b-b154-f8664c49719f)
 Call ID: b47e7320-028a-452b-b154-f8664c49719f
  Args:
    target: :Gosta_von_dem_Bussche-Haddenhausen
    source: :Claus_von_Amsberg
    relation: :hasMother
  AddLiteral (3dca568e-6bfc-4417-a383-759957075852)
 Call ID: 3dca568e-6bfc-4417-a383-759957075852
  Args:
    source: :Claus_von_Amsberg
    relation: :hasBirthYear
    literal_value: 1926
    literal_type: xsd:integer
  AddTriple (384c0cfa-2604-4aba-bdeb-af1382643c41)
 Call ID: 384c0cfa-2604-4aba-bdeb-af1382643c41
  Args:
    relation: :hasBrother
    target: :Julius_von_dem_Bussche-Haddenhausen
    source: :Gosta_von_dem_Bussche-Haddenhausen
  AddLiteral (dee765bb-6a63-4230-a496-20eaad9c04d4)
 Call ID: dee765bb-6a63-4230-a496-20eaad9c04d4
  Args:
    relation: :hasBirthYear
    source: :Julius_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
    literal_value: 1906
  AddLiteral (90ec0fcd-2e8d-45ec-a3de-caf83bb2c867)
 Call ID: 90ec0fcd-2e8d-45ec-a3de-caf83bb2c867
  Args:
    literal_type: xsd:integer
    literal_value: 1977
    relation: :hasDeathYear
    source: :Julius_von_dem_Bussche-Haddenhausen
  AddTriple (8e1664ae-dafd-424d-a162-ee63a1b83976)
 Call ID: 8e1664ae-dafd-424d-a162-ee63a1b83976
  Args:
    relation: :hasFather
    source: :Julius_von_dem_Bussche-Haddenhausen
    target: :George_von_dem_Bussche-Haddenhausen
  AddTriple (acacf41a-4de4-48a8-b8c6-49fff4c7b595)
 Call ID: acacf41a-4de4-48a8-b8c6-49fff4c7b595
  Args:
    source: :Julius_von_dem_Bussche-Haddenhausen
    target: :Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasMother
  AddLiteral (7de795e2-bbcd-41b7-a705-b92f9f128f20)
 Call ID: 7de795e2-bbcd-41b7-a705-b92f9f128f20
  Args:
    source: :Anna-Elisabeth_von_Pfuel
    relation: :hasBirthYear
    literal_value: 1909
    literal_type: xsd:integer
  AddLiteral (6b548795-2f4d-4435-b015-4e7c0d5a9bf3)
 Call ID: 6b548795-2f4d-4435-b015-4e7c0d5a9bf3
  Args:
    literal_value: 2005
    literal_type: xsd:integer
    source: :Anna-Elisabeth_von_Pfuel
    relation: :hasDeathYear
  Finish (7200d65e-052f-49fd-8776-485379c769e7)
 Call ID: 7200d65e-052f-49fd-8776-485379c769e7
  Args: