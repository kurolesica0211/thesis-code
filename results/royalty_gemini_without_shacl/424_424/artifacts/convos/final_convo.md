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
Princess Antonia of Prussia, Duchess of Wellington (Antonia Elizabeth Brigid Louise Mansfeld; born 28 April 1955) is a British aristocrat and philanthropist.
A member of the House of Hohenzollern by birth, she is a great-granddaughter of Wilhelm II, German Emperor and a great-great-great-granddaughter of Queen Victoria of the United Kingdom.
Through her marriage, she is also the Princess of Waterloo, Duchess of Victoria, and Duchess of Ciudad Rodrigo.
Early life and education

Princess Antonia Elizabeth Brigid Louise Mansfeld of Prussia was born in London on 28 April 1955, the daughter of Prince Frederick of Prussia and his wife, Lady Brigid Guinness.
On her father's side, she is a great-granddaughter of the German Emperor Wilhelm II, and granddaughter of Rupert Guinness, 2nd Earl of Iveagh on her mother's side.
Career

In 2007, she was appointed as the President of The Guinness Partnership, an affordable housing charitable society in the United Kingdom, and was appointed an Officer of the Order of the British Empire in the 2008 Birthday Honours for services to social housing.
In 2008 Antonia was appointed as a fellow of Eton College, serving as a member of the college's governing body.
Personal life

On 3 February 1977, she married Charles Wellesley, Marquess of Douro at St Paul's Church, Knightsbridge in London.
Notable guests at the wedding included Queen Elizabeth The Queen Mother, the Prince of Wales, Princess Margaret, and the Duke and Duchess of Kent.
She is godmother to Lady Gabriella Kingston, daughter of Prince & Princess Michael of Kent.
When her husband succeeded his father as the 9th Duke of Wellington, she became the Princess of Waterloo in Belgium and the Netherlands, the Duchess of Victoria in Portugal, the Duchess of Wellington in the United Kingdom, and the Duchess of Ciudad Rodrigo in Spain.
They have five children, including Lady Mary Wellesley and Lady Charlotte Wellesley.


References



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
  AssignClass (f491fc4c-5761-4bff-b7f9-67ab4fe88554)
 Call ID: f491fc4c-5761-4bff-b7f9-67ab4fe88554
  Args:
    type: :Woman
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld_of_Prussia
  AssignClass (4b309994-a58a-4068-976f-a744ab11383f)
 Call ID: 4b309994-a58a-4068-976f-a744ab11383f
  Args:
    type: :Person
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld_of_Prussia
  AddLiteral (3395fb05-b9b9-458d-a6ad-8a43847d3b4a)
 Call ID: 3395fb05-b9b9-458d-a6ad-8a43847d3b4a
  Args:
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld_of_Prussia
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1955
  AssignClass (dedaf630-1e19-49f7-a3aa-a115a90af415)
 Call ID: dedaf630-1e19-49f7-a3aa-a115a90af415
  Args:
    type: :Man
    source: Prince_Frederick_of_Prussia
  AssignClass (5739368b-69b0-42f7-9848-74b59f9c4ae3)
 Call ID: 5739368b-69b0-42f7-9848-74b59f9c4ae3
  Args:
    type: :Person
    source: Prince_Frederick_of_Prussia
  AssignClass (14c9c8b6-255a-401a-a35c-b542703da0d3)
 Call ID: 14c9c8b6-255a-401a-a35c-b542703da0d3
  Args:
    source: Lady_Brigid_Guinness
    type: :Woman
  AssignClass (f7105f7b-73a7-4c05-89ca-4b5296ea7e37)
 Call ID: f7105f7b-73a7-4c05-89ca-4b5296ea7e37
  Args:
    type: :Person
    source: Lady_Brigid_Guinness
  AddTriple (6f39300b-a458-461f-9046-3323047dd46a)
 Call ID: 6f39300b-a458-461f-9046-3323047dd46a
  Args:
    target: Prince_Frederick_of_Prussia
    relation: :hasFather
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld_of_Prussia
  AddTriple (eae9a6a2-25e1-41c9-9c6d-c034d6ea44c3)
 Call ID: eae9a6a2-25e1-41c9-9c6d-c034d6ea44c3
  Args:
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld_of_Prussia
    target: Lady_Brigid_Guinness
    relation: :hasMother
  AssignClass (0507c86a-53cd-4ba1-b17e-ff2ff590543d)
 Call ID: 0507c86a-53cd-4ba1-b17e-ff2ff590543d
  Args:
    type: :Man
    source: Charles_Wellesley
  AssignClass (f673d8cf-ad40-4249-8f52-a4f4eeee2326)
 Call ID: f673d8cf-ad40-4249-8f52-a4f4eeee2326
  Args:
    source: Charles_Wellesley
    type: :Person
  AddLiteral (a27574d7-61a2-4b7c-bdd2-f62142b24617)
 Call ID: a27574d7-61a2-4b7c-bdd2-f62142b24617
  Args:
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld_of_Prussia
    literal_value: 1977
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (088aeda8-4029-4b58-818a-503291abb5b4)
 Call ID: 088aeda8-4029-4b58-818a-503291abb5b4
  Args:
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld_of_Prussia
    target: Charles_Wellesley
    relation: :hasRelation
  AssignClass (8f9f79a1-d5ab-4a12-a40c-c76fc80fb03c)
 Call ID: 8f9f79a1-d5ab-4a12-a40c-c76fc80fb03c
  Args:
    type: :Woman
    source: Lady_Mary_Wellesley
  AssignClass (79b22199-77cc-4173-a257-46191007bb24)
 Call ID: 79b22199-77cc-4173-a257-46191007bb24
  Args:
    source: Lady_Mary_Wellesley
    type: :Person
  AssignClass (b03400b4-e8d3-4d71-86a0-62b46938108a)
 Call ID: b03400b4-e8d3-4d71-86a0-62b46938108a
  Args:
    type: :Woman
    source: Lady_Charlotte_Wellesley
  AssignClass (48b0c98c-9869-4d0e-8645-fbeb79d8b4e3)
 Call ID: 48b0c98c-9869-4d0e-8645-fbeb79d8b4e3
  Args:
    source: Lady_Charlotte_Wellesley
    type: :Person
  AddTriple (6dd02a91-83de-4497-931f-333615edc642)
 Call ID: 6dd02a91-83de-4497-931f-333615edc642
  Args:
    target: Lady_Mary_Wellesley
    relation: :hasChild
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld_of_Prussia
  AddTriple (7a1d2986-cfdf-4475-b412-4eaac0a2eec7)
 Call ID: 7a1d2986-cfdf-4475-b412-4eaac0a2eec7
  Args:
    relation: :hasChild
    target: Lady_Charlotte_Wellesley
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld_of_Prussia
  AddTriple (b9fa1949-0679-4b1a-8d74-dee90fb255a0)
 Call ID: b9fa1949-0679-4b1a-8d74-dee90fb255a0
  Args:
    relation: :hasChild
    target: Lady_Mary_Wellesley
    source: Charles_Wellesley
  AddTriple (86788c08-2a0a-4b4a-9a9d-2761d7e02b81)
 Call ID: 86788c08-2a0a-4b4a-9a9d-2761d7e02b81
  Args:
    target: Lady_Charlotte_Wellesley
    relation: :hasChild
    source: Charles_Wellesley
  AssignClass (442d4a9c-3f76-47de-9f26-3b72eae16803)
 Call ID: 442d4a9c-3f76-47de-9f26-3b72eae16803
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AssignClass (864ff8f0-1a57-42a5-8563-2281b7267ebd)
 Call ID: 864ff8f0-1a57-42a5-8563-2281b7267ebd
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Person
  AddTriple (94969010-b2ba-401d-bc65-bccf6cd476b6)
 Call ID: 94969010-b2ba-401d-bc65-bccf6cd476b6
  Args:
    target: Wilhelm_II_German_Emperor
    relation: :hasAncestor
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld_of_Prussia
  AssignClass (0b1ae788-c8d7-471b-ab12-b7322c6bdc5a)
 Call ID: 0b1ae788-c8d7-471b-ab12-b7322c6bdc5a
  Args:
    type: :Man
    source: Rupert_Guinness_2nd_Earl_of_Iveagh
  AssignClass (d24b66de-0a35-47f0-85cb-ee893c6e00d1)
 Call ID: d24b66de-0a35-47f0-85cb-ee893c6e00d1
  Args:
    type: :Person
    source: Rupert_Guinness_2nd_Earl_of_Iveagh
  AddTriple (8538f859-6eec-46ec-aab5-85569bb6413a)
 Call ID: 8538f859-6eec-46ec-aab5-85569bb6413a
  Args:
    relation: :hasAncestor
    target: Rupert_Guinness_2nd_Earl_of_Iveagh
    source: Lady_Brigid_Guinness
  Finish (f68b56a8-3965-42f1-8c54-993df977ad9a)
 Call ID: f68b56a8-3965-42f1-8c54-993df977ad9a
  Args: