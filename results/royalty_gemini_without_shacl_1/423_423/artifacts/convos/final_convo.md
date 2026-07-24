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
Prince Wilhelm Victor of Prussia (German: Wilhelm Viktor Ernst Freund Friedrich Georg Adalbert; 15 February 1919 – 7 February 1989) was a German royal, soldier and diplomat.
Life

Prince Wilhelm Victor was a grandson of Emperor Wilhelm II and the youngest child of Prince Adalbert of Prussia (1884–1948) and Princess Adelheid "Adi" of Saxe-Meiningen (1891–1971).
His father, Prince Adalbert carried also the title "Graf von Lingen".
His only surviving sister, Princess Viktoria Marina (1917–1981) married Kirby William Patterson (1907–1984).
Marriage

Prince Wilhelm Victor married at Donaueschingen 20 July 1944 Marie Antoinette, Countess of Hoyos-Stichsenstein (Hohenthurm, 27 June 1920 – Marbella 1 March 2004),  daughter of Friedrich, Count of Hoyos-Stichsenstein (1876–1951) and Countess Wilhelmine von Wuthenau-Hohenthurm (1895–1983), niece of Sophie, Duchess of Hohenberg.
They had the following issue:


Death

Prince Wilhelm Viktor died on 7 February 1989 at age 69.



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
  AssignClass (7d4f880c-aa84-49d8-bfea-cb30a15c26e2)
 Call ID: 7d4f880c-aa84-49d8-bfea-cb30a15c26e2
  Args:
    type: :Man
    source: Prince_Wilhelm_Victor_of_Prussia
  AssignClass (8f690b07-a10c-4cc3-b8ee-ba268453f8c2)
 Call ID: 8f690b07-a10c-4cc3-b8ee-ba268453f8c2
  Args:
    type: :Person
    source: Prince_Wilhelm_Victor_of_Prussia
  AddLiteral (5ab96aff-31cf-4ae1-9d57-604209088bb9)
 Call ID: 5ab96aff-31cf-4ae1-9d57-604209088bb9
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1919
    source: Prince_Wilhelm_Victor_of_Prussia
  AddLiteral (dcd0690c-873b-43df-94d6-fa1fcb6d1cb4)
 Call ID: dcd0690c-873b-43df-94d6-fa1fcb6d1cb4
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Wilhelm_Victor_of_Prussia
    literal_value: 1989
  AssignClass (16d2da5f-d01c-4726-b233-91c3dc5eb342)
 Call ID: 16d2da5f-d01c-4726-b233-91c3dc5eb342
  Args:
    type: :Man
    source: Prince_Adalbert_of_Prussia
  AssignClass (4645bc21-0d03-4f17-88db-fa29fb72cc2c)
 Call ID: 4645bc21-0d03-4f17-88db-fa29fb72cc2c
  Args:
    type: :Person
    source: Prince_Adalbert_of_Prussia
  AddLiteral (8c252c3f-8213-4220-8341-8cc425089040)
 Call ID: 8c252c3f-8213-4220-8341-8cc425089040
  Args:
    literal_value: 1884
    source: Prince_Adalbert_of_Prussia
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (7d83c84a-f187-4086-a0e3-9b820a434b21)
 Call ID: 7d83c84a-f187-4086-a0e3-9b820a434b21
  Args:
    literal_value: 1948
    source: Prince_Adalbert_of_Prussia
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (d13fb1ae-1f3b-401d-b610-1e8915f82dda)
 Call ID: d13fb1ae-1f3b-401d-b610-1e8915f82dda
  Args:
    type: :Woman
    source: Princess_Adelheid_of_Saxe-Meiningen
  AssignClass (d4dd63c3-aab5-4218-ba11-23231207ca9e)
 Call ID: d4dd63c3-aab5-4218-ba11-23231207ca9e
  Args:
    type: :Person
    source: Princess_Adelheid_of_Saxe-Meiningen
  AddLiteral (74f79107-8ac5-41c6-b1d8-2635e1506929)
 Call ID: 74f79107-8ac5-41c6-b1d8-2635e1506929
  Args:
    source: Princess_Adelheid_of_Saxe-Meiningen
    literal_value: 1891
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (9a1fdb72-e01a-496f-bdba-9e2770453334)
 Call ID: 9a1fdb72-e01a-496f-bdba-9e2770453334
  Args:
    literal_value: 1971
    source: Princess_Adelheid_of_Saxe-Meiningen
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (5f40f608-200b-4ef9-a722-561f17820a6b)
 Call ID: 5f40f608-200b-4ef9-a722-561f17820a6b
  Args:
    source: Prince_Wilhelm_Victor_of_Prussia
    target: Prince_Adalbert_of_Prussia
    relation: :hasFather
  AddTriple (b491319b-2fea-4b1f-89e6-d921cacbbfd5)
 Call ID: b491319b-2fea-4b1f-89e6-d921cacbbfd5
  Args:
    target: Princess_Adelheid_of_Saxe-Meiningen
    source: Prince_Wilhelm_Victor_of_Prussia
    relation: :hasMother
  AssignClass (033fba8f-9724-4a52-9ce1-9764d02a8126)
 Call ID: 033fba8f-9724-4a52-9ce1-9764d02a8126
  Args:
    type: :Woman
    source: Princess_Viktoria_Marina
  AssignClass (caba2f67-a08e-414b-babb-d69b33b406d2)
 Call ID: caba2f67-a08e-414b-babb-d69b33b406d2
  Args:
    type: :Person
    source: Princess_Viktoria_Marina
  AddLiteral (4796deec-b198-4b11-9386-55e03e43e9f2)
 Call ID: 4796deec-b198-4b11-9386-55e03e43e9f2
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1917
    source: Princess_Viktoria_Marina
  AddLiteral (876496dc-4db4-4f32-bc8d-3a27445cff99)
 Call ID: 876496dc-4db4-4f32-bc8d-3a27445cff99
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Princess_Viktoria_Marina
    literal_value: 1981
  AddTriple (9c23709d-e1c4-43dc-b6f0-20fba4967eb0)
 Call ID: 9c23709d-e1c4-43dc-b6f0-20fba4967eb0
  Args:
    relation: :isSiblingOf
    target: Princess_Viktoria_Marina
    source: Prince_Wilhelm_Victor_of_Prussia
  AssignClass (eadaa0fb-6202-48c9-a859-a31bcf1b0b4c)
 Call ID: eadaa0fb-6202-48c9-a859-a31bcf1b0b4c
  Args:
    type: :Man
    source: Kirby_William_Patterson
  AssignClass (57df2ab7-6427-4231-ba6f-b3c314a04c72)
 Call ID: 57df2ab7-6427-4231-ba6f-b3c314a04c72
  Args:
    type: :Person
    source: Kirby_William_Patterson
  AddLiteral (f37760ba-2755-45a7-b450-3c4f490b45bd)
 Call ID: f37760ba-2755-45a7-b450-3c4f490b45bd
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1907
    source: Kirby_William_Patterson
  AddLiteral (d2763ba0-fb8c-4edb-b8a7-d4ce2508d334)
 Call ID: d2763ba0-fb8c-4edb-b8a7-d4ce2508d334
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1984
    source: Kirby_William_Patterson
  AssignClass (a386a228-59d0-4f0c-81ec-d88b78b202e7)
 Call ID: a386a228-59d0-4f0c-81ec-d88b78b202e7
  Args:
    type: :Woman
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
  AssignClass (54485df9-0cda-4009-b9bc-29febcaa72c4)
 Call ID: 54485df9-0cda-4009-b9bc-29febcaa72c4
  Args:
    type: :Person
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
  AddLiteral (6e4323d5-8969-41aa-9cba-998ea50f338f)
 Call ID: 6e4323d5-8969-41aa-9cba-998ea50f338f
  Args:
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    literal_value: 1920
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (c07b8709-bf52-4950-9c15-268e7d405299)
 Call ID: c07b8709-bf52-4950-9c15-268e7d405299
  Args:
    literal_value: 2004
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (c8c44998-eaf5-4c00-89c8-79725a3eb09a)
 Call ID: c8c44998-eaf5-4c00-89c8-79725a3eb09a
  Args:
    literal_value: 1944
    source: Prince_Wilhelm_Victor_of_Prussia
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (1003ee7f-a386-4dd0-ad7d-afd2e91fb0da)
 Call ID: 1003ee7f-a386-4dd0-ad7d-afd2e91fb0da
  Args:
    relation: :hasRelation
    target: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    source: Prince_Wilhelm_Victor_of_Prussia
  AssignClass (43191c17-764b-4b65-8721-171e1c5d0dd6)
 Call ID: 43191c17-764b-4b65-8721-171e1c5d0dd6
  Args:
    type: :Man
    source: Friedrich_Count_of_Hoyos-Stichsenstein
  AssignClass (4ba1b485-ef3c-49a3-8bdc-2e220ce11b5a)
 Call ID: 4ba1b485-ef3c-49a3-8bdc-2e220ce11b5a
  Args:
    type: :Person
    source: Friedrich_Count_of_Hoyos-Stichsenstein
  AddLiteral (f9fa4ad4-0223-43e4-bc81-e417d7138e0a)
 Call ID: f9fa4ad4-0223-43e4-bc81-e417d7138e0a
  Args:
    literal_value: 1876
    source: Friedrich_Count_of_Hoyos-Stichsenstein
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (c4407361-b104-450f-b333-5f1303530e37)
 Call ID: c4407361-b104-450f-b333-5f1303530e37
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1951
    source: Friedrich_Count_of_Hoyos-Stichsenstein
  AssignClass (b664c000-d351-40f1-91b9-2592073f0d62)
 Call ID: b664c000-d351-40f1-91b9-2592073f0d62
  Args:
    type: :Woman
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
  AssignClass (3282ccb4-ffd7-4286-9ded-264d9cd357dc)
 Call ID: 3282ccb4-ffd7-4286-9ded-264d9cd357dc
  Args:
    type: :Person
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
  AddLiteral (d2a20c52-c319-49fa-9c8c-00896cea7ff5)
 Call ID: d2a20c52-c319-49fa-9c8c-00896cea7ff5
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    literal_value: 1895
  AddLiteral (9327d48d-6676-4e19-8738-0104bbac0d4e)
 Call ID: 9327d48d-6676-4e19-8738-0104bbac0d4e
  Args:
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    literal_value: 1983
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (c25e7781-044c-4709-967c-0ee88105f9d1)
 Call ID: c25e7781-044c-4709-967c-0ee88105f9d1
  Args:
    relation: :hasFather
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    target: Friedrich_Count_of_Hoyos-Stichsenstein
  AddTriple (15847168-2dab-42c7-96c1-6737b1163d1e)
 Call ID: 15847168-2dab-42c7-96c1-6737b1163d1e
  Args:
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    target: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    relation: :hasMother
  Finish (99975f0b-97ab-48c2-bcc6-2889468c9845)
 Call ID: 99975f0b-97ab-48c2-bcc6-2889468c9845
  Args: