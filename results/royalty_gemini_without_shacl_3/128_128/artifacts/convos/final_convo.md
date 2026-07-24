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
  AssignClass (15c89f09-cbf6-4dd9-b96f-6b28487c0138)
 Call ID: 15c89f09-cbf6-4dd9-b96f-6b28487c0138
  Args:
    type: :Woman
    source: Gösta_von_dem_Bussche-Haddenhausen
  AddLiteral (2ca3b7f7-02d4-43a2-a9cc-94d0deaa38fc)
 Call ID: 2ca3b7f7-02d4-43a2-a9cc-94d0deaa38fc
  Args:
    literal_value: 1902
    literal_type: xsd:integer
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasBirthYear
  AddLiteral (159265ac-3bbf-4374-9256-81b945dff968)
 Call ID: 159265ac-3bbf-4374-9256-81b945dff968
  Args:
    literal_type: xsd:integer
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
    literal_value: 1996
  AssignClass (c38f3b4e-dafa-4c19-8ca4-dc583578a690)
 Call ID: c38f3b4e-dafa-4c19-8ca4-dc583578a690
  Args:
    source: George_von_dem_Bussche-Haddenhausen
    type: :Man
  AddLiteral (6256f0a1-81cd-41de-9ec1-e5788adb440d)
 Call ID: 6256f0a1-81cd-41de-9ec1-e5788adb440d
  Args:
    literal_value: 1869
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: George_von_dem_Bussche-Haddenhausen
  AddLiteral (abb13272-663a-44ed-b171-1b4279b69616)
 Call ID: abb13272-663a-44ed-b171-1b4279b69616
  Args:
    source: George_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1923
  AssignClass (4dfd7eee-dcdf-4fd1-a36d-d363c435e538)
 Call ID: 4dfd7eee-dcdf-4fd1-a36d-d363c435e538
  Args:
    type: :Woman
    source: Gabriele_von_dem_Bussche-Ippenburg
  AddLiteral (9ffebc02-8708-4c43-a941-bca367495259)
 Call ID: 9ffebc02-8708-4c43-a941-bca367495259
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Gabriele_von_dem_Bussche-Ippenburg
    literal_value: 1877
  AddLiteral (a074f850-c8f3-4cd4-a6bc-a804c8dd054d)
 Call ID: a074f850-c8f3-4cd4-a6bc-a804c8dd054d
  Args:
    literal_value: 1973
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Gabriele_von_dem_Bussche-Ippenburg
  AddTriple (7f550e03-1248-4ac1-b97c-e123783f58f9)
 Call ID: 7f550e03-1248-4ac1-b97c-e123783f58f9
  Args:
    target: George_von_dem_Bussche-Haddenhausen
    relation: :hasFather
    source: Gösta_von_dem_Bussche-Haddenhausen
  AddTriple (6b6ddd19-5ec3-4628-b88b-f13ee4036444)
 Call ID: 6b6ddd19-5ec3-4628-b88b-f13ee4036444
  Args:
    relation: :hasMother
    source: Gösta_von_dem_Bussche-Haddenhausen
    target: Gabriele_von_dem_Bussche-Ippenburg
  AssignClass (85e22283-7e8a-434c-bf95-e16481450059)
 Call ID: 85e22283-7e8a-434c-bf95-e16481450059
  Args:
    type: :Man
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (b9e94dca-a57b-48e5-ab49-93c31e7f6086)
 Call ID: b9e94dca-a57b-48e5-ab49-93c31e7f6086
  Args:
    literal_value: 1906
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (95be3928-b0f1-4d0d-b47c-bb3220042cf3)
 Call ID: 95be3928-b0f1-4d0d-b47c-bb3220042cf3
  Args:
    literal_value: 1977
    literal_type: xsd:integer
    source: Julius_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
  AddTriple (e481215b-d7b5-4dfc-8751-ff8ae846bfa6)
 Call ID: e481215b-d7b5-4dfc-8751-ff8ae846bfa6
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :isSiblingOf
    target: Julius_von_dem_Bussche-Haddenhausen
  AssignClass (2233bc36-32ef-4e19-95f0-c0cb451dc835)
 Call ID: 2233bc36-32ef-4e19-95f0-c0cb451dc835
  Args:
    source: Claus_Felix_von_Amsberg
    type: :Man
  AddLiteral (db47decd-05be-4187-babd-a35dd64a040b)
 Call ID: db47decd-05be-4187-babd-a35dd64a040b
  Args:
    literal_value: 1890
    relation: :hasBirthYear
    source: Claus_Felix_von_Amsberg
    literal_type: xsd:integer
  AddLiteral (a5d8bbb3-eac3-4e2c-b1b7-a8c57512a944)
 Call ID: a5d8bbb3-eac3-4e2c-b1b7-a8c57512a944
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Claus_Felix_von_Amsberg
    literal_value: 1953
  AddLiteral (78494bac-5f07-4773-9961-bfa14ac5a0e3)
 Call ID: 78494bac-5f07-4773-9961-bfa14ac5a0e3
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1924
  AddTriple (01a29bfe-5588-4e28-88c6-7775b01bf3ed)
 Call ID: 01a29bfe-5588-4e28-88c6-7775b01bf3ed
  Args:
    target: Claus_Felix_von_Amsberg
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasRelation
  AssignClass (00ba0ff8-ac8d-40ea-87b8-c9cb3a8f7f06)
 Call ID: 00ba0ff8-ac8d-40ea-87b8-c9cb3a8f7f06
  Args:
    source: Claus_von_Amsberg
    type: :Man
  AddLiteral (6d76ee5f-d156-4788-b61b-8292145e8523)
 Call ID: 6d76ee5f-d156-4788-b61b-8292145e8523
  Args:
    source: Claus_von_Amsberg
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1926
  AddTriple (99c512be-98d1-43c3-85bd-ec016c4d324a)
 Call ID: 99c512be-98d1-43c3-85bd-ec016c4d324a
  Args:
    relation: :hasSon
    source: Gösta_von_dem_Bussche-Haddenhausen
    target: Claus_von_Amsberg
  AddTriple (5b0c0865-f365-42b1-9ab0-b9d2673d9c47)
 Call ID: 5b0c0865-f365-42b1-9ab0-b9d2673d9c47
  Args:
    target: Claus_Felix_von_Amsberg
    relation: :isSonOf
    source: Claus_von_Amsberg
  AssignClass (b9e6ee99-8bab-43b4-9ce1-c9a13df1a812)
 Call ID: b9e6ee99-8bab-43b4-9ce1-c9a13df1a812
  Args:
    source: Wilhelm_von_Amsberg
    type: :Man
  AssignClass (7c2cc7e7-dd29-4c8f-95ec-748a94a2de1a)
 Call ID: 7c2cc7e7-dd29-4c8f-95ec-748a94a2de1a
  Args:
    type: :Woman
    source: Elise_von_Vieregge
  AddTriple (7dc60c2b-afe8-4dd3-8269-912ea171a23b)
 Call ID: 7dc60c2b-afe8-4dd3-8269-912ea171a23b
  Args:
    target: Wilhelm_von_Amsberg
    relation: :hasFather
    source: Claus_Felix_von_Amsberg
  AddTriple (e5903611-9e4a-47d6-8214-a79af2e88fd7)
 Call ID: e5903611-9e4a-47d6-8214-a79af2e88fd7
  Args:
    source: Claus_Felix_von_Amsberg
    relation: :hasMother
    target: Elise_von_Vieregge
  AssignClass (c48f8966-c3b1-4c1a-b76e-14ff36743b27)
 Call ID: c48f8966-c3b1-4c1a-b76e-14ff36743b27
  Args:
    source: Anna-Elisabeth_von_Pfuel
    type: :Woman
  AddLiteral (5316c868-c768-4e04-8fe5-520670021915)
 Call ID: 5316c868-c768-4e04-8fe5-520670021915
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Anna-Elisabeth_von_Pfuel
    literal_value: 1909
  AddLiteral (b0968458-fc2c-48d8-8808-51ac6b360900)
 Call ID: b0968458-fc2c-48d8-8808-51ac6b360900
  Args:
    literal_value: 2005
    literal_type: xsd:integer
    source: Anna-Elisabeth_von_Pfuel
    relation: :hasDeathYear
  AddTriple (32654c67-1252-4d54-9cf8-f8a4a17dd69b)
 Call ID: 32654c67-1252-4d54-9cf8-f8a4a17dd69b
  Args:
    relation: :hasRelation
    source: Julius_von_dem_Bussche-Haddenhausen
    target: Anna-Elisabeth_von_Pfuel
  Finish (2955aab8-3c3a-489a-b35c-70128bc564f4)
 Call ID: 2955aab8-3c3a-489a-b35c-70128bc564f4
  Args: