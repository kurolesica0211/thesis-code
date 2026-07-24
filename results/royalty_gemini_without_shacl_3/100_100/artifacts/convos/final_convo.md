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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Prince Dimitri Nicholas Paul George Maria of Yugoslavia (born 18 June 1958), also known as Dimitri Karageorgevich or Dimitrije Karađorđević, is a gemologist and member of the Royal House of Yugoslavia.
He founded the jewellery firm bearing his name, Prince Dimitri Company, and continues to serve as its president and creative director.
Life and career

Born in Boulogne-Billancourt, France, Prince Dimitri was raised in Versailles, attending boarding schools in France and Switzerland.
Prince Dimitri began designing jewellery in 1999, with a collection of gemstone cufflinks that was sold at Bergdorf Goodman and Saks Fifth Avenue.
In 2007, he and business partner Todd Morley founded the Prince Dimitri Company, which opened a salon in Manhattan.
Family

Prince Dimitri and Prince Michael of Yugoslavia are the first set of twins born to Prince Alexander of Yugoslavia and his first wife, Princess Maria Pia of Savoy, the eldest daughter of Umberto II of Italy in 1958.
Maria Pia had a second set of twins, Prince Serge and Princess Helene of Yugoslavia in 1963.
They have a younger half-brother, Prince Dushan of Yugoslavia, from their father's second marriage to Princess Barbara of Liechtenstein.
Prince Dimitri belongs to the cadet branch of the Royal House of Yugoslavia, descending from Prince Regent Paul of Yugoslavia.
He is a third cousin of Alexander, Crown Prince of Yugoslavia.
Honours

Ancestry

Dimitri is a member of the House of Karađorđević cadet branch.
He is a great-great-grandson of Prince Alexander of Serbia (reigned 1842–1858).
Through his father, Dimitri descends from kings George I of Greece and Christian IX of Denmark, as well as emperor Alexander II of Russia.
Through his mother, Dimitri descends from kings Umberto II of Italy, Albert I of Belgium, and furthermore from Nicholas I of Montenegro and Miguel I of Portugal.



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
  AssignClass (3e50a302-5dc8-48dc-bc50-024b93199a5b)
 Call ID: 3e50a302-5dc8-48dc-bc50-024b93199a5b
  Args:
    type: :Man
    source: :PrinceDimitriOfYugoslavia
  AssignClass (efaa9738-62d0-40cc-94f5-e32b1f05228b)
 Call ID: efaa9738-62d0-40cc-94f5-e32b1f05228b
  Args:
    type: :Person
    source: :PrinceDimitriOfYugoslavia
  AddLiteral (94c83f69-ca93-4677-afa4-f275b1615ca2)
 Call ID: 94c83f69-ca93-4677-afa4-f275b1615ca2
  Args:
    source: :PrinceDimitriOfYugoslavia
    literal_value: male
    literal_type: xsd:string
    relation: :hasSex
  AddLiteral (9e27fa19-bc4c-4a62-b941-1941443c7800)
 Call ID: 9e27fa19-bc4c-4a62-b941-1941443c7800
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1958
    source: :PrinceDimitriOfYugoslavia
  AddLiteral (383735bf-31c1-4997-b0e9-41aa93dd8687)
 Call ID: 383735bf-31c1-4997-b0e9-41aa93dd8687
  Args:
    literal_value: Dimitri Karageorgevich
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: :PrinceDimitriOfYugoslavia
  AddLiteral (c88974a2-9910-4b3b-9e5a-3be8d0973fda)
 Call ID: c88974a2-9910-4b3b-9e5a-3be8d0973fda
  Args:
    source: :PrinceDimitriOfYugoslavia
    relation: :alsoKnownAs
    literal_type: xsd:string
    literal_value: Dimitrije Karađorđević
  AssignClass (81cc4d9a-30e0-4ffd-9324-7b02e1392dcc)
 Call ID: 81cc4d9a-30e0-4ffd-9324-7b02e1392dcc
  Args:
    type: :Man
    source: :PrinceMichaelOfYugoslavia
  AssignClass (db743beb-4475-438d-a5a8-a6470b4284af)
 Call ID: db743beb-4475-438d-a5a8-a6470b4284af
  Args:
    source: :PrinceMichaelOfYugoslavia
    type: :Person
  AssignClass (4f90b56b-dc7d-4cdc-b857-012a4a963efa)
 Call ID: 4f90b56b-dc7d-4cdc-b857-012a4a963efa
  Args:
    source: :PrinceAlexanderOfYugoslavia
    type: :Man
  AssignClass (16f4fed8-5a30-4baa-94e5-dda8c22043f9)
 Call ID: 16f4fed8-5a30-4baa-94e5-dda8c22043f9
  Args:
    type: :Person
    source: :PrinceAlexanderOfYugoslavia
  AssignClass (06fb0dc2-2389-432b-bace-d7c63daa2e0f)
 Call ID: 06fb0dc2-2389-432b-bace-d7c63daa2e0f
  Args:
    type: :Woman
    source: :PrincessMariaPiaOfSavoy
  AssignClass (19e0b56a-b182-4c59-a37c-7307c84aa8b7)
 Call ID: 19e0b56a-b182-4c59-a37c-7307c84aa8b7
  Args:
    type: :Person
    source: :PrincessMariaPiaOfSavoy
  AddTriple (f13ee6ff-f83d-467c-a640-de11a26e98eb)
 Call ID: f13ee6ff-f83d-467c-a640-de11a26e98eb
  Args:
    target: :PrinceAlexanderOfYugoslavia
    source: :PrinceDimitriOfYugoslavia
    relation: :hasFather
  AddTriple (5e4291c9-1dfc-468e-84cb-886f5aff96f3)
 Call ID: 5e4291c9-1dfc-468e-84cb-886f5aff96f3
  Args:
    source: :PrinceDimitriOfYugoslavia
    relation: :hasMother
    target: :PrincessMariaPiaOfSavoy
  AddTriple (0136fc27-c6f3-4313-98eb-41add6ce2d41)
 Call ID: 0136fc27-c6f3-4313-98eb-41add6ce2d41
  Args:
    target: :PrinceAlexanderOfYugoslavia
    relation: :hasFather
    source: :PrinceMichaelOfYugoslavia
  AddTriple (a11b77d7-6d1f-434a-b3a6-8936e776ef35)
 Call ID: a11b77d7-6d1f-434a-b3a6-8936e776ef35
  Args:
    relation: :hasMother
    source: :PrinceMichaelOfYugoslavia
    target: :PrincessMariaPiaOfSavoy
  AddTriple (09bf1496-296d-4397-80b3-b1b91348c7cd)
 Call ID: 09bf1496-296d-4397-80b3-b1b91348c7cd
  Args:
    source: :PrinceDimitriOfYugoslavia
    relation: :isBrotherOf
    target: :PrinceMichaelOfYugoslavia
  AssignClass (d4566ca4-3c56-460d-b36c-151341d69388)
 Call ID: d4566ca4-3c56-460d-b36c-151341d69388
  Args:
    type: :Man
    source: :UmbertoIIOfItaly
  AssignClass (345aa154-f070-4940-9be8-918c715f9e00)
 Call ID: 345aa154-f070-4940-9be8-918c715f9e00
  Args:
    source: :UmbertoIIOfItaly
    type: :Person
  AddTriple (b8f0e258-f1e5-4689-a42b-164d632af84c)
 Call ID: b8f0e258-f1e5-4689-a42b-164d632af84c
  Args:
    target: :UmbertoIIOfItaly
    source: :PrincessMariaPiaOfSavoy
    relation: :isDaughterOf
  AssignClass (fc5e3d5c-66c1-4aa6-9a1c-fbbacdc85adb)
 Call ID: fc5e3d5c-66c1-4aa6-9a1c-fbbacdc85adb
  Args:
    type: :Man
    source: :PrinceSergeOfYugoslavia
  AssignClass (762db7fb-7091-4f9f-b42f-396142cb46e5)
 Call ID: 762db7fb-7091-4f9f-b42f-396142cb46e5
  Args:
    type: :Person
    source: :PrinceSergeOfYugoslavia
  AssignClass (5332bda3-4cd9-4da4-83b1-3ddc33c28a7f)
 Call ID: 5332bda3-4cd9-4da4-83b1-3ddc33c28a7f
  Args:
    type: :Woman
    source: :PrincessHeleneOfYugoslavia
  AssignClass (6bbaa070-a9ed-4106-9ff1-f21c34462cdc)
 Call ID: 6bbaa070-a9ed-4106-9ff1-f21c34462cdc
  Args:
    type: :Person
    source: :PrincessHeleneOfYugoslavia
  AddTriple (d7c2bdf6-6ae9-4d01-9443-a35b07c16606)
 Call ID: d7c2bdf6-6ae9-4d01-9443-a35b07c16606
  Args:
    target: :PrincessMariaPiaOfSavoy
    source: :PrinceSergeOfYugoslavia
    relation: :hasMother
  AddTriple (583ffdbd-fb14-47af-b8f2-6acc2ce7bdd3)
 Call ID: 583ffdbd-fb14-47af-b8f2-6acc2ce7bdd3
  Args:
    source: :PrincessHeleneOfYugoslavia
    relation: :hasMother
    target: :PrincessMariaPiaOfSavoy
  AssignClass (48397117-267d-43c9-8754-2a15601e5feb)
 Call ID: 48397117-267d-43c9-8754-2a15601e5feb
  Args:
    type: :Man
    source: :PrinceDushanOfYugoslavia
  AssignClass (97e62b5d-edb4-469c-955c-749a74e298cf)
 Call ID: 97e62b5d-edb4-469c-955c-749a74e298cf
  Args:
    source: :PrinceDushanOfYugoslavia
    type: :Person
  AssignClass (71d3d8e9-7b61-4d22-a5a4-c57d57b78010)
 Call ID: 71d3d8e9-7b61-4d22-a5a4-c57d57b78010
  Args:
    source: :PrincessBarbaraOfLiechtenstein
    type: :Woman
  AssignClass (04d13f1d-3e65-49b1-950c-258ba3db3f1f)
 Call ID: 04d13f1d-3e65-49b1-950c-258ba3db3f1f
  Args:
    type: :Person
    source: :PrincessBarbaraOfLiechtenstein
  AddTriple (17bb6a2f-46e5-495a-857a-ac813cba9f0d)
 Call ID: 17bb6a2f-46e5-495a-857a-ac813cba9f0d
  Args:
    source: :PrinceDushanOfYugoslavia
    relation: :hasFather
    target: :PrinceAlexanderOfYugoslavia
  AddTriple (1778c71b-92e1-4874-a9cb-64fd7242f65f)
 Call ID: 1778c71b-92e1-4874-a9cb-64fd7242f65f
  Args:
    source: :PrinceDushanOfYugoslavia
    relation: :hasMother
    target: :PrincessBarbaraOfLiechtenstein
  AssignClass (064951fd-b62a-4dab-80e6-77fdce9ac747)
 Call ID: 064951fd-b62a-4dab-80e6-77fdce9ac747
  Args:
    type: :Man
    source: :PrinceRegentPaulOfYugoslavia
  AssignClass (bdb1ce7a-749f-4b84-9ce5-ae26c779863e)
 Call ID: bdb1ce7a-749f-4b84-9ce5-ae26c779863e
  Args:
    type: :Person
    source: :PrinceRegentPaulOfYugoslavia
  AddTriple (34eadb8c-032b-43bb-8675-2c7ecf15f6d4)
 Call ID: 34eadb8c-032b-43bb-8675-2c7ecf15f6d4
  Args:
    target: :PrinceRegentPaulOfYugoslavia
    source: :PrinceDimitriOfYugoslavia
    relation: :hasAncestor
  AssignClass (18f4a0e8-cf9b-4f62-b999-fa9ad27e14b3)
 Call ID: 18f4a0e8-cf9b-4f62-b999-fa9ad27e14b3
  Args:
    type: :Man
    source: :AlexanderCrownPrinceOfYugoslavia
  AssignClass (90254856-ad64-4a97-b7c2-25df0497b86f)
 Call ID: 90254856-ad64-4a97-b7c2-25df0497b86f
  Args:
    source: :AlexanderCrownPrinceOfYugoslavia
    type: :Person
  AddTriple (bfadc5b4-b681-439e-b8be-2c4dbd1b51f1)
 Call ID: bfadc5b4-b681-439e-b8be-2c4dbd1b51f1
  Args:
    relation: :isBloodrelationOf
    source: :PrinceDimitriOfYugoslavia
    target: :AlexanderCrownPrinceOfYugoslavia
  AssignClass (0bc50a7f-63d4-4b6b-ac44-7b15609f71ee)
 Call ID: 0bc50a7f-63d4-4b6b-ac44-7b15609f71ee
  Args:
    type: :Man
    source: :PrinceAlexanderOfSerbia
  AssignClass (5a4e7094-a783-48d1-8291-f37bb73ba0c7)
 Call ID: 5a4e7094-a783-48d1-8291-f37bb73ba0c7
  Args:
    type: :Person
    source: :PrinceAlexanderOfSerbia
  AddTriple (400a5e89-2e94-45b3-8de0-17beddbe3abf)
 Call ID: 400a5e89-2e94-45b3-8de0-17beddbe3abf
  Args:
    source: :PrinceDimitriOfYugoslavia
    relation: :hasAncestor
    target: :PrinceAlexanderOfSerbia
  Finish (ec3edcfc-cd73-4b5d-ab29-3f2ec3a1ced9)
 Call ID: ec3edcfc-cd73-4b5d-ab29-3f2ec3a1ced9
  Args: