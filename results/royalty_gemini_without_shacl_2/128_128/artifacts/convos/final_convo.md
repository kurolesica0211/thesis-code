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
  AssignClass (308a5f26-9b30-40e2-9b69-1499ce09450c)
 Call ID: 308a5f26-9b30-40e2-9b69-1499ce09450c
  Args:
    type: :Woman
    source: Gösta_von_dem_Bussche-Haddenhausen
  AddLiteral (d4702471-891b-43de-a3e7-ac58abb0f920)
 Call ID: d4702471-891b-43de-a3e7-ac58abb0f920
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1902
  AddLiteral (f5585fc6-fd6a-424f-b6a4-941a6eeebe63)
 Call ID: f5585fc6-fd6a-424f-b6a4-941a6eeebe63
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1996
  AssignClass (b2d64411-dffb-4a73-9bac-e73ff4ac32df)
 Call ID: b2d64411-dffb-4a73-9bac-e73ff4ac32df
  Args:
    source: George_von_dem_Bussche-Haddenhausen
    type: :Man
  AddLiteral (742dc547-7136-4850-8332-766aca4c3c65)
 Call ID: 742dc547-7136-4850-8332-766aca4c3c65
  Args:
    source: George_von_dem_Bussche-Haddenhausen
    literal_value: 1869
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (750fbf0b-e79f-4a2c-9264-dba083f7c46d)
 Call ID: 750fbf0b-e79f-4a2c-9264-dba083f7c46d
  Args:
    source: George_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1923
  AssignClass (4bdb9bee-6543-455a-ab98-c6fc7dc529e1)
 Call ID: 4bdb9bee-6543-455a-ab98-c6fc7dc529e1
  Args:
    type: :Woman
    source: Gabriele_von_dem_Bussche-Ippenburg
  AddLiteral (a3c069c0-8633-4402-aa8d-5f20866ecfe6)
 Call ID: a3c069c0-8633-4402-aa8d-5f20866ecfe6
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1877
  AddLiteral (b454e64e-2180-4c4a-a3ef-27ba9acc677d)
 Call ID: b454e64e-2180-4c4a-a3ef-27ba9acc677d
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1973
  AddTriple (4b334484-e0d9-493d-a231-80a0f22f8a32)
 Call ID: 4b334484-e0d9-493d-a231-80a0f22f8a32
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    target: George_von_dem_Bussche-Haddenhausen
    relation: :hasFather
  AddTriple (16a99c3e-49c2-4c73-a472-1ed19b0645e1)
 Call ID: 16a99c3e-49c2-4c73-a472-1ed19b0645e1
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasMother
    target: Gabriele_von_dem_Bussche-Ippenburg
  AssignClass (2b9650e0-44fe-417b-a42c-10dbe05e679c)
 Call ID: 2b9650e0-44fe-417b-a42c-10dbe05e679c
  Args:
    source: Claus_Felix_von_Amsberg
    type: :Man
  AddLiteral (0ca4be0b-51cd-4b6b-b548-daca65fa5684)
 Call ID: 0ca4be0b-51cd-4b6b-b548-daca65fa5684
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1890
    source: Claus_Felix_von_Amsberg
  AddLiteral (790ec950-5675-42f4-95c3-09472a2e38ea)
 Call ID: 790ec950-5675-42f4-95c3-09472a2e38ea
  Args:
    source: Claus_Felix_von_Amsberg
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1953
  AddLiteral (bf8c7121-5ec2-4b2b-9c1d-ab962635dd4a)
 Call ID: bf8c7121-5ec2-4b2b-9c1d-ab962635dd4a
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    literal_value: 1924
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (b4e519c8-9cd6-4e99-b71f-ec56c42113cb)
 Call ID: b4e519c8-9cd6-4e99-b71f-ec56c42113cb
  Args:
    relation: :hasRelation
    target: Claus_Felix_von_Amsberg
    source: Gösta_von_dem_Bussche-Haddenhausen
  AssignClass (7d777eef-524d-409f-93e7-f457803df04e)
 Call ID: 7d777eef-524d-409f-93e7-f457803df04e
  Args:
    type: :Man
    source: Claus_von_Amsberg
  AddLiteral (f3d7dd58-2ca6-49fd-953a-781e260c64d7)
 Call ID: f3d7dd58-2ca6-49fd-953a-781e260c64d7
  Args:
    source: Claus_von_Amsberg
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1926
  AddTriple (c59f72f7-729a-4f38-a046-f6cadacdc0a6)
 Call ID: c59f72f7-729a-4f38-a046-f6cadacdc0a6
  Args:
    source: Claus_von_Amsberg
    relation: :hasMother
    target: Gösta_von_dem_Bussche-Haddenhausen
  AddTriple (c0e46616-44e1-47fd-aaf0-c902dc0b5159)
 Call ID: c0e46616-44e1-47fd-aaf0-c902dc0b5159
  Args:
    source: Claus_von_Amsberg
    relation: :hasFather
    target: Claus_Felix_von_Amsberg
  AssignClass (0c04ae5c-318d-4c08-a80e-a4d3fa087baa)
 Call ID: 0c04ae5c-318d-4c08-a80e-a4d3fa087baa
  Args:
    type: :Man
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (5d085291-058a-4faa-aa5a-dd47c3bd49dd)
 Call ID: 5d085291-058a-4faa-aa5a-dd47c3bd49dd
  Args:
    literal_value: 1906
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (c862d9c6-a2b9-4213-adc3-1eb622fe2301)
 Call ID: c862d9c6-a2b9-4213-adc3-1eb622fe2301
  Args:
    source: Julius_von_dem_Bussche-Haddenhausen
    literal_value: 1977
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (6e8e00e5-2535-4b9d-8532-59c0d90f8e84)
 Call ID: 6e8e00e5-2535-4b9d-8532-59c0d90f8e84
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasBrother
    target: Julius_von_dem_Bussche-Haddenhausen
  AddTriple (20ce0646-6b4e-4296-be7a-aec90493f55c)
 Call ID: 20ce0646-6b4e-4296-be7a-aec90493f55c
  Args:
    source: Julius_von_dem_Bussche-Haddenhausen
    relation: :hasFather
    target: George_von_dem_Bussche-Haddenhausen
  AddTriple (feb7d387-00a0-492f-ba6c-4bd605dbccfc)
 Call ID: feb7d387-00a0-492f-ba6c-4bd605dbccfc
  Args:
    target: Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasMother
    source: Julius_von_dem_Bussche-Haddenhausen
  AssignClass (2ed416e8-bbaf-49fa-9801-08a11cd25da8)
 Call ID: 2ed416e8-bbaf-49fa-9801-08a11cd25da8
  Args:
    type: :Man
    source: Wilhelm_von_Amsberg
  AssignClass (da9f0f4e-f643-4039-9fb8-c5a041a1cff7)
 Call ID: da9f0f4e-f643-4039-9fb8-c5a041a1cff7
  Args:
    type: :Woman
    source: Elise_von_Vieregge
  AddTriple (09760f5d-aa98-44d4-8376-9ab875e75e74)
 Call ID: 09760f5d-aa98-44d4-8376-9ab875e75e74
  Args:
    source: Claus_Felix_von_Amsberg
    relation: :hasFather
    target: Wilhelm_von_Amsberg
  AddTriple (d9e4927e-3dd3-4eb1-9b61-b0cf8b472368)
 Call ID: d9e4927e-3dd3-4eb1-9b61-b0cf8b472368
  Args:
    relation: :hasMother
    target: Elise_von_Vieregge
    source: Claus_Felix_von_Amsberg
  AssignClass (ca4c95a7-804f-453a-80d6-3d429dad37b0)
 Call ID: ca4c95a7-804f-453a-80d6-3d429dad37b0
  Args:
    type: :Woman
    source: Anna-Elisabeth_von_Pfuel
  AddLiteral (1450cb03-d86e-4508-a139-c86ee2d95fdd)
 Call ID: 1450cb03-d86e-4508-a139-c86ee2d95fdd
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1909
    source: Anna-Elisabeth_von_Pfuel
  AddLiteral (7bd2dde3-1d79-47b6-b31f-8580096d39aa)
 Call ID: 7bd2dde3-1d79-47b6-b31f-8580096d39aa
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2005
    source: Anna-Elisabeth_von_Pfuel
  AddTriple (4d10d38c-9b82-4746-b808-a20e07156881)
 Call ID: 4d10d38c-9b82-4746-b808-a20e07156881
  Args:
    source: Julius_von_dem_Bussche-Haddenhausen
    relation: :hasRelation
    target: Anna-Elisabeth_von_Pfuel
  AssignClass (bf1a9613-3ef1-4a8a-b72e-011034f48b3d)
 Call ID: bf1a9613-3ef1-4a8a-b72e-011034f48b3d
  Args:
    source: Eberhard_Friedrich_Gustav_von_dem_Bussche-Ippenburg
    type: :Man
  AddTriple (be8cd60d-d346-4829-b4f3-60c30d89a456)
 Call ID: be8cd60d-d346-4829-b4f3-60c30d89a456
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    target: Eberhard_Friedrich_Gustav_von_dem_Bussche-Ippenburg
    relation: :hasFather
  AssignClass (bab49680-ecb5-4a57-b34f-029f56519339)
 Call ID: bab49680-ecb5-4a57-b34f-029f56519339
  Args:
    type: :Woman
    source: Armgard_von_Cramm
  AssignClass (29bf0af1-6a87-4342-b66e-934e75f59143)
 Call ID: 29bf0af1-6a87-4342-b66e-934e75f59143
  Args:
    type: :Man
    source: Aschwin_of_Sierstorpff-Cramm
  AddLiteral (5f30d37a-d45b-42f3-8a51-2373b6bc876c)
 Call ID: 5f30d37a-d45b-42f3-8a51-2373b6bc876c
  Args:
    source: Aschwin_of_Sierstorpff-Cramm
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1846
  AddLiteral (6673a82e-2782-4296-8812-73393b1890bf)
 Call ID: 6673a82e-2782-4296-8812-73393b1890bf
  Args:
    literal_value: 1909
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Aschwin_of_Sierstorpff-Cramm
  AssignClass (7a9c5ee3-a1ff-42bf-bbdb-0ba22a6f9ad9)
 Call ID: 7a9c5ee3-a1ff-42bf-bbdb-0ba22a6f9ad9
  Args:
    source: Hedwig_von_Sierstorpff-Driburg
    type: :Woman
  AddLiteral (c027b1a3-3991-4158-9cae-d319df31fbb0)
 Call ID: c027b1a3-3991-4158-9cae-d319df31fbb0
  Args:
    source: Hedwig_von_Sierstorpff-Driburg
    literal_value: 1848
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (3dcb2463-a9f1-4b8e-a95c-6a130878ab90)
 Call ID: 3dcb2463-a9f1-4b8e-a95c-6a130878ab90
  Args:
    source: Hedwig_von_Sierstorpff-Driburg
    literal_value: 1900
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (5228f28a-b902-4cb6-ac18-01daef72e8d6)
 Call ID: 5228f28a-b902-4cb6-ac18-01daef72e8d6
  Args:
    target: Aschwin_of_Sierstorpff-Cramm
    relation: :hasFather
    source: Armgard_von_Cramm
  AddTriple (00665b2f-9100-488a-a38b-505d4e1df0bb)
 Call ID: 00665b2f-9100-488a-a38b-505d4e1df0bb
  Args:
    target: Hedwig_von_Sierstorpff-Driburg
    relation: :hasMother
    source: Armgard_von_Cramm
  AssignClass (4c3a89e2-41eb-45dc-9f05-21e0fda6d2ff)
 Call ID: 4c3a89e2-41eb-45dc-9f05-21e0fda6d2ff
  Args:
    type: :Woman
    source: Hedwig_von_Sierstorpff-Cramm
  AddLiteral (056fe96d-34d2-4095-87a3-784b9b60d25f)
 Call ID: 056fe96d-34d2-4095-87a3-784b9b60d25f
  Args:
    source: Hedwig_von_Sierstorpff-Cramm
    literal_value: 1874
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (3d9965f0-e3cf-48b1-8924-93ec17ce6fe2)
 Call ID: 3d9965f0-e3cf-48b1-8924-93ec17ce6fe2
  Args:
    literal_value: 1907
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Hedwig_von_Sierstorpff-Cramm
  AddTriple (b62ebaac-b851-4beb-a3d6-3204dd0ee42e)
 Call ID: b62ebaac-b851-4beb-a3d6-3204dd0ee42e
  Args:
    source: Hedwig_von_Sierstorpff-Cramm
    relation: :hasFather
    target: Aschwin_of_Sierstorpff-Cramm
  AddTriple (c9eec260-60bd-4b04-bb54-43e03f02c824)
 Call ID: c9eec260-60bd-4b04-bb54-43e03f02c824
  Args:
    target: Hedwig_von_Sierstorpff-Driburg
    relation: :hasMother
    source: Hedwig_von_Sierstorpff-Cramm
  Finish (9e01dce0-2d68-4c7d-8811-b74e5fe1d24c)
 Call ID: 9e01dce0-2d68-4c7d-8811-b74e5fe1d24c
  Args: