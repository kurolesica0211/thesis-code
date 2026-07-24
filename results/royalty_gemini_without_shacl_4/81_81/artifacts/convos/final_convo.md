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
Prince Vincent of Denmark, Count of Monpezat RE (Vincent Frederik Minik Alexander; born 8 January 2011) is a member of the Danish royal family.
He is the third child and younger son of King Frederik X and Queen Mary, the sixth grandchild and youngest grandson of Queen Margrethe II and Prince Henrik, and the older twin brother of Princess Josephine.
Vincent is third in line to the Danish throne, after his older brother, Crown Prince Christian, and older sister, Princess Isabella.
Birth and early life

Queen Margrethe II


Vincent was born on 8 January 2011 at Rigshospitalet, the Copenhagen University Hospital, in Copenhagen, at 10:30 am local time, 26 minutes before his twin sister.
Shortly after the birth, while speaking to the press, the Crown Prince joked about calling his newborn son Elvis, as the twins share a birthday with Elvis Presley.
Vincent and his sister were baptised by the royal confessor, the Bishop of Copenhagen Erik Norman Svendsen, on 14 April at the Church of Holmen in central Copenhagen.
The twins were baptised at the royal baptismal font which has been used for the baptism of royal children in Denmark since 1671.
Prince Vincent wore the royal christening gown which was made for his great-great-grandfather, King Christian X, in 1870, while his sister wore a gown found among Queen Ingrid's belongings.
His name was announced as Vincent Frederik Minik Alexander.
His godparents are his maternal uncle, John Stuart Donaldson; his father's first cousin, the Prince of Sayn-Wittgenstein-Berleburg (then the Hereditary Prince); his mother's lady-in-waiting, Caroline Heering; and friends of his parents, the King of Spain (then the Prince of Asturias), Count Michael Ahlefeldt-Laurvig-Bille and Baroness Helle Reedtz-Thott.
Under the old system of male-preference primogeniture, Vincent would have displaced his elder sister Isabella in the line of succession; with the new law, he comes directly after her instead.
On 15 August 2017, Vincent and his younger twin sister started school at Tranegårdsskolen in Gentofte – the same public school as their elder siblings.
Titles, styles, and honours

Vincent is styled as His Royal Highness Prince Vincent of Denmark, Count of Monpezat.



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
  AssignClass (3f2a4d25-847b-4b12-bb89-3b45d81482d9)
 Call ID: 3f2a4d25-847b-4b12-bb89-3b45d81482d9
  Args:
    source: :Prince_Vincent_of_Denmark
    type: :Man
  AssignClass (11a92154-f4d1-422d-bcff-2188ce83a52b)
 Call ID: 11a92154-f4d1-422d-bcff-2188ce83a52b
  Args:
    source: :Prince_Vincent_of_Denmark
    type: :Person
  AddLiteral (fe1f86ff-42c4-4154-8358-7bacb149f723)
 Call ID: fe1f86ff-42c4-4154-8358-7bacb149f723
  Args:
    source: :Prince_Vincent_of_Denmark
    literal_type: xsd:integer
    literal_value: 2011
    relation: :hasBirthYear
  AssignClass (27d2b204-34f0-41ac-a94c-dcd41cdca447)
 Call ID: 27d2b204-34f0-41ac-a94c-dcd41cdca447
  Args:
    type: :Man
    source: :King_Frederik_X
  AssignClass (8b10d9c9-a71a-46ca-a851-5a8d049b885c)
 Call ID: 8b10d9c9-a71a-46ca-a851-5a8d049b885c
  Args:
    type: :Person
    source: :King_Frederik_X
  AssignClass (88fd84e5-f659-4241-ab7e-b2f52af90388)
 Call ID: 88fd84e5-f659-4241-ab7e-b2f52af90388
  Args:
    type: :Woman
    source: :Queen_Mary
  AssignClass (84aecbe2-a8fa-439a-8617-8171536bcc2c)
 Call ID: 84aecbe2-a8fa-439a-8617-8171536bcc2c
  Args:
    source: :Queen_Mary
    type: :Person
  AddTriple (81e5ffe6-df07-42c8-9a30-0d2a5105fd0a)
 Call ID: 81e5ffe6-df07-42c8-9a30-0d2a5105fd0a
  Args:
    target: :King_Frederik_X
    relation: :hasFather
    source: :Prince_Vincent_of_Denmark
  AddTriple (1add2858-00ef-44e8-94af-f347b7c8a1f7)
 Call ID: 1add2858-00ef-44e8-94af-f347b7c8a1f7
  Args:
    target: :Queen_Mary
    relation: :hasMother
    source: :Prince_Vincent_of_Denmark
  AssignClass (5f51bfc2-4339-4ce2-b51f-0704f0af642f)
 Call ID: 5f51bfc2-4339-4ce2-b51f-0704f0af642f
  Args:
    type: :Woman
    source: :Princess_Josephine
  AssignClass (819b83ad-1fb8-490e-ae58-073221f48c95)
 Call ID: 819b83ad-1fb8-490e-ae58-073221f48c95
  Args:
    source: :Princess_Josephine
    type: :Person
  AddTriple (8d86e5aa-f78e-4979-b0c9-ee829faf2a3f)
 Call ID: 8d86e5aa-f78e-4979-b0c9-ee829faf2a3f
  Args:
    source: :Prince_Vincent_of_Denmark
    target: :Princess_Josephine
    relation: :isSiblingOf
  AssignClass (6f723e6d-9ffb-4ca1-b199-f739910ba8d7)
 Call ID: 6f723e6d-9ffb-4ca1-b199-f739910ba8d7
  Args:
    type: :Woman
    source: :Queen_Margrethe_II
  AssignClass (62387e88-9e51-4b95-916b-c27fbc948815)
 Call ID: 62387e88-9e51-4b95-916b-c27fbc948815
  Args:
    type: :Person
    source: :Queen_Margrethe_II
  AssignClass (49ddf6c8-4fc8-4634-a949-96dcf9610b0a)
 Call ID: 49ddf6c8-4fc8-4634-a949-96dcf9610b0a
  Args:
    type: :Man
    source: :Prince_Henrik
  AssignClass (a0f5348e-f804-4fd4-bce4-064843e85d72)
 Call ID: a0f5348e-f804-4fd4-bce4-064843e85d72
  Args:
    type: :Person
    source: :Prince_Henrik
  AddTriple (2bb233f8-f237-4d0d-9051-9b348edd7f9e)
 Call ID: 2bb233f8-f237-4d0d-9051-9b348edd7f9e
  Args:
    source: :King_Frederik_X
    target: :Queen_Margrethe_II
    relation: :hasParent
  AddTriple (97a95179-7114-4a35-8593-b0434e44f385)
 Call ID: 97a95179-7114-4a35-8593-b0434e44f385
  Args:
    relation: :hasParent
    target: :Prince_Henrik
    source: :King_Frederik_X
  AssignClass (c64268f0-fa5b-4012-b251-0a1dff2d9bd2)
 Call ID: c64268f0-fa5b-4012-b251-0a1dff2d9bd2
  Args:
    type: :Man
    source: :Crown_Prince_Christian
  AssignClass (28ec0c6d-5b59-48b6-9ee8-b27ff71510e7)
 Call ID: 28ec0c6d-5b59-48b6-9ee8-b27ff71510e7
  Args:
    source: :Crown_Prince_Christian
    type: :Person
  AddTriple (aa66f472-fd43-462f-9771-9fcc268465c4)
 Call ID: aa66f472-fd43-462f-9771-9fcc268465c4
  Args:
    relation: :isSiblingOf
    target: :Crown_Prince_Christian
    source: :Prince_Vincent_of_Denmark
  AssignClass (1e66062f-1545-4064-9625-950d255fc978)
 Call ID: 1e66062f-1545-4064-9625-950d255fc978
  Args:
    source: :Princess_Isabella
    type: :Woman
  AssignClass (29496995-453f-4e1f-8b5e-c81fbce8e714)
 Call ID: 29496995-453f-4e1f-8b5e-c81fbce8e714
  Args:
    type: :Person
    source: :Princess_Isabella
  AddTriple (af317681-e5de-42d9-aa31-76b46db04611)
 Call ID: af317681-e5de-42d9-aa31-76b46db04611
  Args:
    source: :Prince_Vincent_of_Denmark
    target: :Princess_Isabella
    relation: :isSiblingOf
  AssignClass (d6a99a65-c84a-47e8-99fb-2dfa55a0efc5)
 Call ID: d6a99a65-c84a-47e8-99fb-2dfa55a0efc5
  Args:
    source: :King_Christian_X
    type: :Man
  AssignClass (33210179-6e44-493f-b266-a27b3c2fe6cf)
 Call ID: 33210179-6e44-493f-b266-a27b3c2fe6cf
  Args:
    type: :Person
    source: :King_Christian_X
  AssignClass (98787a32-83ec-430b-a21a-51f58d011876)
 Call ID: 98787a32-83ec-430b-a21a-51f58d011876
  Args:
    type: :Woman
    source: :Queen_Ingrid
  AssignClass (a3aae6ef-22ca-4038-82cc-161847992cc9)
 Call ID: a3aae6ef-22ca-4038-82cc-161847992cc9
  Args:
    type: :Person
    source: :Queen_Ingrid
  Finish (583175bc-85fb-4e61-a2af-bbca8cf93b25)
 Call ID: 583175bc-85fb-4e61-a2af-bbca8cf93b25
  Args: