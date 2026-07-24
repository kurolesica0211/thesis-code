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
Princess María de las Mercedes of Bourbon-Two Sicilies (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Spanish: ; María de las Mercedes Cristina Genara Isabel Luisa Carolina Victoria y Todos los Santos de Borbón y Orléans; 23 December 1910 – 2 January 2000) was a member of the Spanish royal family and the mother of King Juan Carlos I.


The daughter of Prince Carlos of Bourbon-Two Sicilies and Princess Louise of Orléans, she married Infante Juan, Count of Barcelona, claimant to the Spanish throne.
Biography

María was born in Madrid, daughter of Prince Carlos of Bourbon-Two Sicilies, Infante of Spain, a grandson of King Ferdinand II of the Two Sicilies, and his second wife, Princess Louise of Orléans, daughter of Prince Philippe, Count of Paris, a pretender to the French throne.
She was granted, at birth, the rank and precedence of an infanta of Spain, although not the actual use of the title, her own being Princess of Bourbon-Two Sicilies.
When the Second Spanish Republic forced them into exile, they lived in Cannes and later in Paris, where she studied art at the Louvre.
On 14 January 1935, she attended the wedding, in Rome, of Infanta Beatriz of Spain, daughter of King Alfonso XIII, to Alessandro Torlonia, 5th Prince of Civitella-Cesi.
There she met the brother of the bride, her third cousin and future husband, the Infante Juan, fourth son and designated heir of Alfonso XIII.
When her husband took up Count of Barcelona as a title of pretence on 8 March 1941, María became the Countess of Barcelona.
They lived in Cannes and Rome, and, with the outbreak of World War II, they moved to Lausanne to live with Queen Victoria Eugenie, the mother of Infante Juan.
In 1953, the Countess represented the Spanish Royal Family at the coronation of Queen Elizabeth II.
In 1976, one year after the monarchy was restored in Spain in the person of her son, Juan Carlos, they returned to Spain.
She mediated between her son and her husband, estranged since Juan Carlos had been designated heir by Franco.
In 1977, Juan renounced his rights in favour of their son, who officially allowed him to retain the title of Count of Barcelona.
In 1995, her granddaughter Infanta Elena married in Seville in part because the Countess' love for the city.



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
  AssignClass (1c529f05-8dc4-489a-9b75-42dc806fb3fb)
 Call ID: 1c529f05-8dc4-489a-9b75-42dc806fb3fb
  Args:
    type: :Woman
    source: María_de_las_Mercedes_de_Borbón-Dos_Sicilias
  AssignClass (83479880-cf37-4dcd-b753-537c4a1a790b)
 Call ID: 83479880-cf37-4dcd-b753-537c4a1a790b
  Args:
    source: María_de_las_Mercedes_de_Borbón-Dos_Sicilias
    type: :Person
  AddLiteral (d4e4e97f-1048-4bfb-84ab-146a107b70ed)
 Call ID: d4e4e97f-1048-4bfb-84ab-146a107b70ed
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1910
    source: María_de_las_Mercedes_de_Borbón-Dos_Sicilias
  AddLiteral (147d8ac3-78ef-4374-83de-4ee4837eefbb)
 Call ID: 147d8ac3-78ef-4374-83de-4ee4837eefbb
  Args:
    literal_type: xsd:integer
    literal_value: 2000
    relation: :hasDeathYear
    source: María_de_las_Mercedes_de_Borbón-Dos_Sicilias
  AssignClass (7110f2e2-4cbb-4215-acaa-41815d234eac)
 Call ID: 7110f2e2-4cbb-4215-acaa-41815d234eac
  Args:
    source: Juan_Carlos_I
    type: :Man
  AssignClass (d566c9b8-82d7-44e3-b189-35f44bf098ca)
 Call ID: d566c9b8-82d7-44e3-b189-35f44bf098ca
  Args:
    type: :Person
    source: Juan_Carlos_I
  AddTriple (eb410e58-327c-443e-bfd0-a4c34adefe0b)
 Call ID: eb410e58-327c-443e-bfd0-a4c34adefe0b
  Args:
    relation: :isMotherOf
    target: Juan_Carlos_I
    source: María_de_las_Mercedes_de_Borbón-Dos_Sicilias
  AssignClass (173a7bd0-1ab7-49e6-a1c0-25269b4785bb)
 Call ID: 173a7bd0-1ab7-49e6-a1c0-25269b4785bb
  Args:
    type: :Man
    source: Carlos_de_Borbón-Dos_Sicilias
  AssignClass (b2a3ca96-0dc9-43a0-9826-849c724146d2)
 Call ID: b2a3ca96-0dc9-43a0-9826-849c724146d2
  Args:
    type: :Person
    source: Carlos_de_Borbón-Dos_Sicilias
  AssignClass (e3c964f7-e374-41f1-8212-d1fe45632916)
 Call ID: e3c964f7-e374-41f1-8212-d1fe45632916
  Args:
    source: Carlos_de_Borbón-Dos_Sicilias
    type: :Ancestor
  AssignClass (80f9cf9b-e629-4fa2-b278-7cc8d2b1d2c1)
 Call ID: 80f9cf9b-e629-4fa2-b278-7cc8d2b1d2c1
  Args:
    source: Louise_of_Orléans
    type: :Woman
  AssignClass (74cae0df-b7c2-4adf-b7f4-8f4997c86d5b)
 Call ID: 74cae0df-b7c2-4adf-b7f4-8f4997c86d5b
  Args:
    source: Louise_of_Orléans
    type: :Person
  AssignClass (8b679183-0ec4-4f68-88ca-9ced2a0dadd7)
 Call ID: 8b679183-0ec4-4f68-88ca-9ced2a0dadd7
  Args:
    type: :Ancestor
    source: Louise_of_Orléans
  AddTriple (9d5aa4ac-441b-4678-9ce9-a392b19382e5)
 Call ID: 9d5aa4ac-441b-4678-9ce9-a392b19382e5
  Args:
    relation: :isFatherOf
    target: María_de_las_Mercedes_de_Borbón-Dos_Sicilias
    source: Carlos_de_Borbón-Dos_Sicilias
  AddTriple (8bd332cf-ebf8-4180-98a2-ad092ca77a7e)
 Call ID: 8bd332cf-ebf8-4180-98a2-ad092ca77a7e
  Args:
    source: Louise_of_Orléans
    target: María_de_las_Mercedes_de_Borbón-Dos_Sicilias
    relation: :isMotherOf
  AssignClass (941ae6d0-2039-497c-aed5-1ddc7f75d1b2)
 Call ID: 941ae6d0-2039-497c-aed5-1ddc7f75d1b2
  Args:
    source: Juan_Count_of_Barcelona
    type: :Man
  AssignClass (9ea6a3f1-4326-401e-8199-ec1398d53d5d)
 Call ID: 9ea6a3f1-4326-401e-8199-ec1398d53d5d
  Args:
    source: Juan_Count_of_Barcelona
    type: :Person
  AddTriple (82aef8dc-5fae-4a03-948c-5745d089b600)
 Call ID: 82aef8dc-5fae-4a03-948c-5745d089b600
  Args:
    source: María_de_las_Mercedes_de_Borbón-Dos_Sicilias
    target: Juan_Count_of_Barcelona
    relation: :hasRelation
  AssignClass (1721812d-0f05-4d17-9093-ac4adabcf4e6)
 Call ID: 1721812d-0f05-4d17-9093-ac4adabcf4e6
  Args:
    type: :Man
    source: Ferdinand_II_of_the_Two_Sicilies
  AssignClass (c6b9a006-16fc-4516-bb2e-ca62b8b6a4ed)
 Call ID: c6b9a006-16fc-4516-bb2e-ca62b8b6a4ed
  Args:
    source: Ferdinand_II_of_the_Two_Sicilies
    type: :Person
  AssignClass (c2509a3a-7db9-48f6-9f0e-ec3dcd3c3d39)
 Call ID: c2509a3a-7db9-48f6-9f0e-ec3dcd3c3d39
  Args:
    type: :Ancestor
    source: Ferdinand_II_of_the_Two_Sicilies
  AddTriple (2d7cfe3d-4aea-4b84-88e1-5e5a4878148b)
 Call ID: 2d7cfe3d-4aea-4b84-88e1-5e5a4878148b
  Args:
    source: Ferdinand_II_of_the_Two_Sicilies
    target: Carlos_de_Borbón-Dos_Sicilias
    relation: :isFatherOf
  AssignClass (7a6c8d2d-0788-453b-8310-9854ee545d7e)
 Call ID: 7a6c8d2d-0788-453b-8310-9854ee545d7e
  Args:
    type: :Man
    source: Philippe_Count_of_Paris
  AssignClass (59f2b246-6cc3-4d67-b846-7e0740422450)
 Call ID: 59f2b246-6cc3-4d67-b846-7e0740422450
  Args:
    type: :Person
    source: Philippe_Count_of_Paris
  AssignClass (16226d97-cbf3-47fd-aa5c-e04c0c7035b5)
 Call ID: 16226d97-cbf3-47fd-aa5c-e04c0c7035b5
  Args:
    type: :Ancestor
    source: Philippe_Count_of_Paris
  AddTriple (07b4d2e3-862d-4af2-b6e8-d8a626ddeceb)
 Call ID: 07b4d2e3-862d-4af2-b6e8-d8a626ddeceb
  Args:
    source: Philippe_Count_of_Paris
    target: Louise_of_Orléans
    relation: :isFatherOf
  AssignClass (121967ed-c38c-4307-bfdc-0678404b296d)
 Call ID: 121967ed-c38c-4307-bfdc-0678404b296d
  Args:
    source: Beatriz_of_Spain
    type: :Woman
  AssignClass (54ba8f69-cb67-46a0-894b-0fc6ca27bce7)
 Call ID: 54ba8f69-cb67-46a0-894b-0fc6ca27bce7
  Args:
    type: :Person
    source: Beatriz_of_Spain
  AssignClass (c998a137-b60e-469b-bd0d-d4642459099b)
 Call ID: c998a137-b60e-469b-bd0d-d4642459099b
  Args:
    source: Alfonso_XIII
    type: :Man
  AssignClass (73b33bd0-6050-4ea4-8b9c-21dd1bcd3631)
 Call ID: 73b33bd0-6050-4ea4-8b9c-21dd1bcd3631
  Args:
    type: :Person
    source: Alfonso_XIII
  AssignClass (2e09b3f5-92d4-43c8-9f5c-f1b3c2b08c95)
 Call ID: 2e09b3f5-92d4-43c8-9f5c-f1b3c2b08c95
  Args:
    source: Alfonso_XIII
    type: :Ancestor
  AddTriple (13d5ac2d-36dc-4996-9c0f-9d66fd4bf7b4)
 Call ID: 13d5ac2d-36dc-4996-9c0f-9d66fd4bf7b4
  Args:
    source: Alfonso_XIII
    target: Beatriz_of_Spain
    relation: :isFatherOf
  AddTriple (132acfb7-9edc-49fd-83fa-04d45abb5ef3)
 Call ID: 132acfb7-9edc-49fd-83fa-04d45abb5ef3
  Args:
    source: Alfonso_XIII
    target: Juan_Count_of_Barcelona
    relation: :isFatherOf
  AddTriple (6184ccd3-5685-4b34-928f-1bb8558c7e94)
 Call ID: 6184ccd3-5685-4b34-928f-1bb8558c7e94
  Args:
    target: Beatriz_of_Spain
    relation: :isBrotherOf
    source: Juan_Count_of_Barcelona
  AssignClass (96d905ea-5a73-4f8e-b5c9-792c3bffe218)
 Call ID: 96d905ea-5a73-4f8e-b5c9-792c3bffe218
  Args:
    source: Alessandro_Torlonia
    type: :Man
  AssignClass (3788d77b-bf01-4355-8b45-7046c64adbe5)
 Call ID: 3788d77b-bf01-4355-8b45-7046c64adbe5
  Args:
    type: :Person
    source: Alessandro_Torlonia
  AddTriple (dc3dafd4-9077-45ef-8351-a6f210b6f9b3)
 Call ID: dc3dafd4-9077-45ef-8351-a6f210b6f9b3
  Args:
    relation: :hasRelation
    target: Alessandro_Torlonia
    source: Beatriz_of_Spain
  AssignClass (ca723b55-27ec-4d56-b2a1-2c391fb5eac5)
 Call ID: ca723b55-27ec-4d56-b2a1-2c391fb5eac5
  Args:
    source: Victoria_Eugenie
    type: :Woman
  AssignClass (487e9e60-ff78-4780-ba07-ec434639b317)
 Call ID: 487e9e60-ff78-4780-ba07-ec434639b317
  Args:
    source: Victoria_Eugenie
    type: :Person
  AssignClass (de9d13b9-2f52-4f3d-a114-98f7d8f752e1)
 Call ID: de9d13b9-2f52-4f3d-a114-98f7d8f752e1
  Args:
    type: :Ancestor
    source: Victoria_Eugenie
  AddTriple (0c817481-68cf-4839-9a09-a4f3f32519bb)
 Call ID: 0c817481-68cf-4839-9a09-a4f3f32519bb
  Args:
    source: Victoria_Eugenie
    target: Juan_Count_of_Barcelona
    relation: :isMotherOf
  AssignClass (7dd40d45-33ef-4cf2-b4bb-fc0eca433fc3)
 Call ID: 7dd40d45-33ef-4cf2-b4bb-fc0eca433fc3
  Args:
    source: Elena_of_Spain
    type: :Woman
  AssignClass (27a85b97-85cd-4d22-8eb5-db77b0e5327f)
 Call ID: 27a85b97-85cd-4d22-8eb5-db77b0e5327f
  Args:
    type: :Person
    source: Elena_of_Spain
  AddTriple (9e5ba2eb-e237-487f-9e85-cf03c03c6909)
 Call ID: 9e5ba2eb-e237-487f-9e85-cf03c03c6909
  Args:
    source: María_de_las_Mercedes_de_Borbón-Dos_Sicilias
    target: Elena_of_Spain
    relation: :isMotherOf
  Finish (e3f2b2d6-1625-4f5a-9116-3422a42d04d5)
 Call ID: e3f2b2d6-1625-4f5a-9116-3422a42d04d5
  Args: