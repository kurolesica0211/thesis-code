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
Sir David Bowes-Lyon (2 May 1902 – 13 September 1961) was a British aristocrat who was the younger brother of Queen Elizabeth the Queen Mother and uncle to Queen Elizabeth II.
Early life

David Bowes-Lyon was born on 2 May 1902.
He was the tenth and youngest child, and the sixth son, of Claude Bowes-Lyon, 14th
His paternal grandparents were Claude Bowes-Lyon, 13th
Career

During World War II, Bowes-Lyon was a member of the secret propaganda department Political Warfare Executive.
On 15 December 1948, Bowes-Lyon attended the christening of his great-nephew Prince Charles.
He was one of eight sponsors of the prince, along with King George VI, King Haakon VII of Norway, Queen Mary, Princess Margaret, the Dowager Marchioness of Milford Haven, Patricia, Lady Brabourne, and Prince George of Greece and Denmark.
As a keen gardener, Bowes-Lyon was awarded the Victoria Medal of Honour in 1953 and served as president of the Royal Horticultural Society from 1953 to 1961.
Bowes-Lyon was made a Knight Commander of the Royal Victorian Order in the 1959 Birthday Honours.
Personal life

On 6 February 1929, David Bowes-Lyon married Rachel Pauline Spender-Clay (1907–1996), younger daughter of Herbert Henry Spender-Clay and Pauline Spender-Clay.
Together, they had two children:


Bowes-Lyon died at his sister Elizabeth's home, Birkhall, on the Balmoral estate, of a heart attack after suffering from hemiplegia on 13 September 1961, aged 59.
The Queen Mother discovered him dead in bed.



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
  AssignClass (5c9f4b6d-9c49-4330-a819-e1e44b321c56)
 Call ID: 5c9f4b6d-9c49-4330-a819-e1e44b321c56
  Args:
    type: :Man
    source: :David_Bowes-Lyon
  AssignClass (b33eb24e-b295-47e5-a481-9fb2acb137f1)
 Call ID: b33eb24e-b295-47e5-a481-9fb2acb137f1
  Args:
    type: :Person
    source: :David_Bowes-Lyon
  AddLiteral (7863e4d1-d88a-4d32-b45b-334f5992df52)
 Call ID: 7863e4d1-d88a-4d32-b45b-334f5992df52
  Args:
    literal_value: 1902
    relation: :hasBirthYear
    source: :David_Bowes-Lyon
    literal_type: xsd:integer
  AddLiteral (bf3c8d26-7862-4c15-9df1-a4748339f621)
 Call ID: bf3c8d26-7862-4c15-9df1-a4748339f621
  Args:
    literal_value: 1961
    relation: :hasDeathYear
    source: :David_Bowes-Lyon
    literal_type: xsd:integer
  AssignClass (3c6da9bc-f214-47b4-bc34-58284a9879b2)
 Call ID: 3c6da9bc-f214-47b4-bc34-58284a9879b2
  Args:
    type: :Woman
    source: :Queen_Elizabeth_the_Queen_Mother
  AssignClass (4e2b6357-fa05-41cf-9b4f-a708c63c4d77)
 Call ID: 4e2b6357-fa05-41cf-9b4f-a708c63c4d77
  Args:
    type: :Person
    source: :Queen_Elizabeth_the_Queen_Mother
  AddTriple (4d164cfe-e9ed-43d1-85e0-0d7b70ae5d78)
 Call ID: 4d164cfe-e9ed-43d1-85e0-0d7b70ae5d78
  Args:
    target: :Queen_Elizabeth_the_Queen_Mother
    relation: :hasSister
    source: :David_Bowes-Lyon
  AssignClass (7b15f47c-ee24-44ec-825f-86c56404067d)
 Call ID: 7b15f47c-ee24-44ec-825f-86c56404067d
  Args:
    type: :Woman
    source: :Queen_Elizabeth_II
  AssignClass (40f69255-31e3-498d-a8a9-40179cae2c8b)
 Call ID: 40f69255-31e3-498d-a8a9-40179cae2c8b
  Args:
    type: :Person
    source: :Queen_Elizabeth_II
  AddTriple (541888a7-2123-4645-916a-c740761a6851)
 Call ID: 541888a7-2123-4645-916a-c740761a6851
  Args:
    target: :Queen_Elizabeth_II
    source: :David_Bowes-Lyon
    relation: :isUncleOf
  AssignClass (4fb5751e-d20c-4e17-9a6c-ac13963dbcf7)
 Call ID: 4fb5751e-d20c-4e17-9a6c-ac13963dbcf7
  Args:
    type: :Man
    source: :Claude_Bowes-Lyon_14th
  AssignClass (19d51114-1c55-459a-96d1-0121b68af2b6)
 Call ID: 19d51114-1c55-459a-96d1-0121b68af2b6
  Args:
    type: :Person
    source: :Claude_Bowes-Lyon_14th
  AddTriple (41392f55-ae84-4c4b-a2ca-e081ce68ccfe)
 Call ID: 41392f55-ae84-4c4b-a2ca-e081ce68ccfe
  Args:
    relation: :isFatherOf
    source: :Claude_Bowes-Lyon_14th
    target: :David_Bowes-Lyon
  AssignClass (750d6783-8849-4fdb-a3d9-3b097dd982e7)
 Call ID: 750d6783-8849-4fdb-a3d9-3b097dd982e7
  Args:
    type: :Man
    source: :Claude_Bowes-Lyon_13th
  AssignClass (788e56b7-3fc4-45db-b3cc-d95a2e27b142)
 Call ID: 788e56b7-3fc4-45db-b3cc-d95a2e27b142
  Args:
    type: :Person
    source: :Claude_Bowes-Lyon_13th
  AddTriple (ddc46b42-3e32-4944-8178-f2167021aaa9)
 Call ID: ddc46b42-3e32-4944-8178-f2167021aaa9
  Args:
    target: :Claude_Bowes-Lyon_14th
    relation: :isFatherOf
    source: :Claude_Bowes-Lyon_13th
  AssignClass (100d156c-5d35-49d3-931c-c1c874a159c8)
 Call ID: 100d156c-5d35-49d3-931c-c1c874a159c8
  Args:
    type: :Woman
    source: :Rachel_Pauline_Spender-Clay
  AssignClass (cc742ed6-28df-4b19-9bb0-22016ee075c6)
 Call ID: cc742ed6-28df-4b19-9bb0-22016ee075c6
  Args:
    type: :Person
    source: :Rachel_Pauline_Spender-Clay
  AddLiteral (746c3f2f-8ee0-441d-97fd-c35fcb06d93a)
 Call ID: 746c3f2f-8ee0-441d-97fd-c35fcb06d93a
  Args:
    literal_value: 1929
    relation: :hasMarriageYear
    source: :David_Bowes-Lyon
    literal_type: xsd:integer
  AddTriple (c5c3e13f-cb28-48fa-ae47-11a24deb032d)
 Call ID: c5c3e13f-cb28-48fa-ae47-11a24deb032d
  Args:
    target: :Rachel_Pauline_Spender-Clay
    source: :David_Bowes-Lyon
    relation: :hasRelation
  AssignClass (8c135f67-a58c-4bed-a1cc-b8b5d236faab)
 Call ID: 8c135f67-a58c-4bed-a1cc-b8b5d236faab
  Args:
    type: :Man
    source: :Herbert_Henry_Spender-Clay
  AssignClass (fbeb4425-e7c6-4e5f-8247-b87ce7551c2c)
 Call ID: fbeb4425-e7c6-4e5f-8247-b87ce7551c2c
  Args:
    type: :Person
    source: :Herbert_Henry_Spender-Clay
  AddTriple (3bb600ad-8434-4f12-8687-ccf13ddd6a65)
 Call ID: 3bb600ad-8434-4f12-8687-ccf13ddd6a65
  Args:
    target: :Rachel_Pauline_Spender-Clay
    source: :Herbert_Henry_Spender-Clay
    relation: :isFatherOf
  AssignClass (63dbb42f-2b59-4367-8f87-43ac25dbd0fd)
 Call ID: 63dbb42f-2b59-4367-8f87-43ac25dbd0fd
  Args:
    type: :Woman
    source: :Pauline_Spender-Clay
  AssignClass (f92ffd94-ea6b-4d16-a4ed-e578e6dd85cb)
 Call ID: f92ffd94-ea6b-4d16-a4ed-e578e6dd85cb
  Args:
    type: :Person
    source: :Pauline_Spender-Clay
  AddTriple (0684cf5e-4a90-49e6-a4d2-315c455b7bb4)
 Call ID: 0684cf5e-4a90-49e6-a4d2-315c455b7bb4
  Args:
    relation: :isMotherOf
    source: :Pauline_Spender-Clay
    target: :Rachel_Pauline_Spender-Clay
  Finish (b80d1b01-de97-4ee8-9104-6655a06bb85e)
 Call ID: b80d1b01-de97-4ee8-9104-6655a06bb85e
  Args: