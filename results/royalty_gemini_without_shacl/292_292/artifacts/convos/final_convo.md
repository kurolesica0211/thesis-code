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
Princess Christina of the Netherlands (Maria Christina; 18 February 1947 – 16 August 2019) was the youngest of four daughters of Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld.
She taught singing in New York and was a long-term supporter of the Youth Music Foundation in the Netherlands.
Christina died of bone cancer in 2019.
Early life

Princess Christina, who was known as Princess Marijke in her youth, was born on 18 February 1947, at Soestdijk Palace, Baarn, the Netherlands.
Her parents were Crown Princess Juliana, the only child of Queen Wilhelmina of the Netherlands, and Prince Bernhard of Lippe-Biesterfeld.
At the time of her birth, she was fifth in the line to the throne after her mother and three older sisters: Princess Beatrix, Princess Irene and Princess Margriet.
She was baptised on 9 October 1947 and her godparents included Queen Wilhelmina (her maternal grandmother), her eldest sister Princess Beatrix, Sir Winston Churchill (for whom her father stood proxy), her paternal grandmother Princess Armgard of Lippe-Biesterfeld, Prince Felix of Luxembourg, and his niece Princess Anne of Bourbon-Parma.
On 4 September 1948, after a reign of nearly 58 years, Christina's grandmother Queen Wilhelmina (68) abdicated the throne and her mother was inaugurated as Queen of the Kingdom of the Netherlands on 6 September 1948.
Childhood and education

While her mother was pregnant with Christina, she contracted either measles or rubella and as a result, Christina was born nearly blind.
In 1963, she stopped using her first name Maria, from then on referring to herself merely as Christina.
Marriage

While living in New York as Christina van Oranje, the Princess started a relationship with Cuban exile Jorge Guillermo.
Although societal attitudes were changing, because Guillermo was a Catholic, it was still possible that a marriage could cause a public scandal in the Netherlands such as the one that occurred in 1964 when Christina's sister Princess Irene married the Catholic Prince Carlos Hugo of Bourbon-Parma.
Accordingly, Princess Christina, at that time ninth in line for the Dutch throne, renounced her and her descendants' rights to the throne before officially announcing her engagement on St. Valentine's Day, 1975.
After their wedding, they lived in New York but later moved to the Netherlands, where they built Villa Eikenhorst  in Wassenaar, near The Hague.
She recorded and released several CDs (classical, Broadway) in 2000 and 2002, and was a long-term supporter of the Youth Music Foundation in the Netherlands.
In 1989, she allowed her name to be used for the Prinses Christina Concours, an annual competition held in the Netherlands to encourage the musical talents of children in the Netherlands.
One of her few public performances was at the marriage of her nephew Prince Bernhard Jr.
She also sang at the funerals of both of her parents Princess Juliana and Prince Bernhard in the New Church (Delft).
Early 2019, Christina made headlines when she decided to sell several works of art.
These works came to her through inheritance from the Dutch royal family: art lover William II of the Netherlands.
Death

In June 2018, it was announced that Princess Christina had been diagnosed with bone cancer.
Titles, styles and honours

Honours

National honours

Foreign honours

Ancestry

References

External links

2 also Princess of Lippe-Biesterfeld



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
  AssignClass (ae092d2b-6774-4a52-8ec5-f7a35d4f720d)
 Call ID: ae092d2b-6774-4a52-8ec5-f7a35d4f720d
  Args:
    type: :Woman
    source: Princess_Christina_of_the_Netherlands
  AssignClass (73bc7d58-a6cf-4373-8e68-8e13a8b07489)
 Call ID: 73bc7d58-a6cf-4373-8e68-8e13a8b07489
  Args:
    type: :Person
    source: Princess_Christina_of_the_Netherlands
  AddLiteral (abdbce82-ad81-4bd7-9c02-ed7ab51b2b5e)
 Call ID: abdbce82-ad81-4bd7-9c02-ed7ab51b2b5e
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Princess_Christina_of_the_Netherlands
    literal_value: 1947
  AddLiteral (2eb60887-bea9-464a-b430-f76a49b038f5)
 Call ID: 2eb60887-bea9-464a-b430-f76a49b038f5
  Args:
    source: Princess_Christina_of_the_Netherlands
    literal_type: xsd:integer
    literal_value: 2019
    relation: :hasDeathYear
  AddLiteral (0da5bbd9-bade-42ca-ae16-fa43b921802d)
 Call ID: 0da5bbd9-bade-42ca-ae16-fa43b921802d
  Args:
    source: Princess_Christina_of_the_Netherlands
    literal_type: xsd:string
    literal_value: Maria Christina
    relation: :alsoKnownAs
  AddLiteral (2bcba3a0-c477-41f3-8577-13fed7f74e38)
 Call ID: 2bcba3a0-c477-41f3-8577-13fed7f74e38
  Args:
    literal_value: Princess Marijke
    literal_type: xsd:string
    source: Princess_Christina_of_the_Netherlands
    relation: :alsoKnownAs
  AssignClass (ccdb0b2a-6cb3-48a4-b688-a6bcec1a6899)
 Call ID: ccdb0b2a-6cb3-48a4-b688-a6bcec1a6899
  Args:
    type: :Woman
    source: Queen_Juliana_of_the_Netherlands
  AssignClass (bd77d06d-1d7e-4170-b3bc-4001d1acfd06)
 Call ID: bd77d06d-1d7e-4170-b3bc-4001d1acfd06
  Args:
    source: Queen_Juliana_of_the_Netherlands
    type: :Person
  AssignClass (c8132164-2854-497a-8c4e-8d766c01c3c4)
 Call ID: c8132164-2854-497a-8c4e-8d766c01c3c4
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (d09da7a1-4fe5-4ccc-ba09-fa9f7c7cefd3)
 Call ID: d09da7a1-4fe5-4ccc-ba09-fa9f7c7cefd3
  Args:
    type: :Person
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AddTriple (e3c5497e-971c-402c-826f-d3886e2128c1)
 Call ID: e3c5497e-971c-402c-826f-d3886e2128c1
  Args:
    relation: :hasMother
    target: Queen_Juliana_of_the_Netherlands
    source: Princess_Christina_of_the_Netherlands
  AddTriple (dbc96819-1a12-4050-9476-47928fd07ffc)
 Call ID: dbc96819-1a12-4050-9476-47928fd07ffc
  Args:
    relation: :hasFather
    target: Prince_Bernhard_of_Lippe-Biesterfeld
    source: Princess_Christina_of_the_Netherlands
  AssignClass (03d723d2-ac8c-4041-a748-7101dcceb5d3)
 Call ID: 03d723d2-ac8c-4041-a748-7101dcceb5d3
  Args:
    type: :Woman
    source: Queen_Wilhelmina_of_the_Netherlands
  AssignClass (05364eee-70a6-4788-a1b5-8d18649f4c63)
 Call ID: 05364eee-70a6-4788-a1b5-8d18649f4c63
  Args:
    type: :Person
    source: Queen_Wilhelmina_of_the_Netherlands
  AddTriple (3faac86a-7a57-4f1b-972d-46262d12951a)
 Call ID: 3faac86a-7a57-4f1b-972d-46262d12951a
  Args:
    target: Queen_Wilhelmina_of_the_Netherlands
    relation: :hasMother
    source: Queen_Juliana_of_the_Netherlands
  AssignClass (743eb735-c7ee-48ca-872d-83a76b993d03)
 Call ID: 743eb735-c7ee-48ca-872d-83a76b993d03
  Args:
    type: :Woman
    source: Princess_Beatrix
  AssignClass (a86c58aa-7056-4c09-bb03-a8c88f2190a7)
 Call ID: a86c58aa-7056-4c09-bb03-a8c88f2190a7
  Args:
    type: :Person
    source: Princess_Beatrix
  AssignClass (fde3ec37-93de-46e9-9a49-d1223323bf47)
 Call ID: fde3ec37-93de-46e9-9a49-d1223323bf47
  Args:
    source: Princess_Irene
    type: :Woman
  AssignClass (d8e579d1-d762-4ebf-91e0-1a02eb653af5)
 Call ID: d8e579d1-d762-4ebf-91e0-1a02eb653af5
  Args:
    type: :Person
    source: Princess_Irene
  AssignClass (7123569f-948b-4f19-92b4-51d7029eca5d)
 Call ID: 7123569f-948b-4f19-92b4-51d7029eca5d
  Args:
    type: :Woman
    source: Princess_Margriet
  AssignClass (188bf5f6-0ea5-4c42-b408-5bb66549263f)
 Call ID: 188bf5f6-0ea5-4c42-b408-5bb66549263f
  Args:
    type: :Person
    source: Princess_Margriet
  AddTriple (c7b4070a-3b7d-4e7a-8b9c-22ec1a46b539)
 Call ID: c7b4070a-3b7d-4e7a-8b9c-22ec1a46b539
  Args:
    source: Princess_Christina_of_the_Netherlands
    target: Princess_Beatrix
    relation: :isSisterOf
  AddTriple (35ac6be3-2578-493c-bdb2-3c470ecd828e)
 Call ID: 35ac6be3-2578-493c-bdb2-3c470ecd828e
  Args:
    source: Princess_Christina_of_the_Netherlands
    target: Princess_Irene
    relation: :isSisterOf
  AddTriple (8fd3d8a2-cd1c-4815-865f-eee22ab0601d)
 Call ID: 8fd3d8a2-cd1c-4815-865f-eee22ab0601d
  Args:
    relation: :isSisterOf
    target: Princess_Margriet
    source: Princess_Christina_of_the_Netherlands
  AssignClass (1840b4cc-b13b-4a84-97fe-299cdaaae208)
 Call ID: 1840b4cc-b13b-4a84-97fe-299cdaaae208
  Args:
    type: :Man
    source: Jorge_Guillermo
  AssignClass (2e8fe293-d81d-4467-a71c-74e29ba332cb)
 Call ID: 2e8fe293-d81d-4467-a71c-74e29ba332cb
  Args:
    source: Jorge_Guillermo
    type: :Person
  AddLiteral (bf82e3a9-0e2c-429d-9c3a-ff79b6b9ad41)
 Call ID: bf82e3a9-0e2c-429d-9c3a-ff79b6b9ad41
  Args:
    relation: :hasMarriageYear
    literal_value: 1975
    source: Princess_Christina_of_the_Netherlands
    literal_type: xsd:integer
  AddTriple (2f8203e2-9edc-4fb0-801d-47377a9d4e95)
 Call ID: 2f8203e2-9edc-4fb0-801d-47377a9d4e95
  Args:
    relation: :hasRelation
    target: Jorge_Guillermo
    source: Princess_Christina_of_the_Netherlands
  AssignClass (dcd17740-5f5b-4478-aa7c-206ecb44f78f)
 Call ID: dcd17740-5f5b-4478-aa7c-206ecb44f78f
  Args:
    source: Prince_Carlos_Hugo_of_Bourbon-Parma
    type: :Man
  AssignClass (1f10a7ef-a5c0-47a0-a7db-14b8bfb733e4)
 Call ID: 1f10a7ef-a5c0-47a0-a7db-14b8bfb733e4
  Args:
    source: Prince_Carlos_Hugo_of_Bourbon-Parma
    type: :Person
  AddTriple (8423b28b-dc4f-4140-bc15-bc996e442a4c)
 Call ID: 8423b28b-dc4f-4140-bc15-bc996e442a4c
  Args:
    relation: :hasRelation
    target: Prince_Carlos_Hugo_of_Bourbon-Parma
    source: Princess_Irene
  AssignClass (8493e9a0-b520-4f60-95ba-791b4e3a72a6)
 Call ID: 8493e9a0-b520-4f60-95ba-791b4e3a72a6
  Args:
    source: Princess_Armgard_of_Lippe-Biesterfeld
    type: :Woman
  AssignClass (b9c4f48f-ed21-4519-b4b1-061dc36ca2b4)
 Call ID: b9c4f48f-ed21-4519-b4b1-061dc36ca2b4
  Args:
    type: :Person
    source: Princess_Armgard_of_Lippe-Biesterfeld
  AssignClass (fa7d75f1-49ba-42cb-b594-209ae179f442)
 Call ID: fa7d75f1-49ba-42cb-b594-209ae179f442
  Args:
    source: Prince_Felix_of_Luxembourg
    type: :Man
  AssignClass (bba490e2-6cfd-45db-bf15-fe9660a4e173)
 Call ID: bba490e2-6cfd-45db-bf15-fe9660a4e173
  Args:
    type: :Person
    source: Prince_Felix_of_Luxembourg
  AssignClass (4bbe096f-eee2-4414-a9c6-639c9f555497)
 Call ID: 4bbe096f-eee2-4414-a9c6-639c9f555497
  Args:
    type: :Woman
    source: Princess_Anne_of_Bourbon-Parma
  AssignClass (cee945e9-9367-473d-8154-866cb570617e)
 Call ID: cee945e9-9367-473d-8154-866cb570617e
  Args:
    type: :Person
    source: Princess_Anne_of_Bourbon-Parma
  AssignClass (506a9376-5755-46ac-b3db-ece5fd97d111)
 Call ID: 506a9376-5755-46ac-b3db-ece5fd97d111
  Args:
    type: :Man
    source: Prince_Bernhard_Jr
  AssignClass (b58b0a98-2747-487d-9beb-aee02eba0d14)
 Call ID: b58b0a98-2747-487d-9beb-aee02eba0d14
  Args:
    source: Prince_Bernhard_Jr
    type: :Person
  AssignClass (1151232f-3fd7-4d70-96b7-fe3978a53a39)
 Call ID: 1151232f-3fd7-4d70-96b7-fe3978a53a39
  Args:
    type: :Man
    source: William_II_of_the_Netherlands
  AssignClass (0ae2bc21-32c0-406b-8d09-8a15994fe1c2)
 Call ID: 0ae2bc21-32c0-406b-8d09-8a15994fe1c2
  Args:
    type: :Person
    source: William_II_of_the_Netherlands
  Finish (8fb36290-c4bf-48ce-9497-58305a699d95)
 Call ID: 8fb36290-c4bf-48ce-9497-58305a699d95
  Args: