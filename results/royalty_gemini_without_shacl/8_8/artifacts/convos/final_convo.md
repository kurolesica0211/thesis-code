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
Lady Sarah Frances Elizabeth Chatto (née Armstrong-Jones; born 1
She is the only daughter of Princess Margaret, Countess of Snowdon, and Antony Armstrong-Jones, 1st Earl of Snowdon.
She and her brother, David Armstrong-Jones, 2nd Earl of Snowdon, are the only maternal first cousins of King Charles III.
Early life and education

Lady Sarah Frances Elizabeth Armstrong-Jones was born at 8:20 am on 1 May 1964 at Kensington Palace in London.
She is the second child and only daughter of Princess Margaret and Antony Armstrong-Jones, 1st Earl of Snowdon.
Sarah is a godmother to Prince Harry, Duke of Sussex, Lady Rose Gilman, and Lady Louise Windsor.
She also has half-siblings on her father's side: Polly Fry (born 1960), Lady Frances Armstrong-Jones (born 1979), and Jasper Cable-Alexander (born 1998).
Sarah and her brother, David, then Viscount Linley, grew up in the nursery of Kensington Palace, Apartment 10.
Their parents' marriage was fractious; the couple formally separated when Sarah was 12 and divorced when she was 14.
Holidays were given to the royal estates at Sandringham and Balmoral, where Sarah did landscape painting.
Sarah was a bridesmaid at the wedding of her cousin Charles, Prince of Wales, and Lady Diana Spencer.
The film's producer, her relative John Knatchbull, 7th Baron Brabourne (son-in-law of Louis Mountbatten, 1st Earl Mountbatten of Burma), gave her a job as an intern assisting the wardrobe department and studying wood gilding under her father's cousin Thomas Messel.
Professional life

Chatto has been exhibiting her work, always under the name Sarah Armstrong-Jones, at The Redfern Gallery since 1995.
Chatto does not undertake public duties and is not considered a "working royal".
However, it has been reported that she was close to her aunt Queen Elizabeth II.
Chatto is frequently seen attending public events such as jubilees and funerals, as well as semi-private royal family events, such as the Sandringham Christmas service, with her sons.
Marriage and children

Sarah met Daniel Chatto during her years in India with her father in the 1980s.
Chatto was working on another British film, Heat and Dust.
He is from a theatrical family, the son of actor Tom Chatto (1920–1982) and the theatrical agent Ros Chatto (born Rosalind Joan Thompson; died 2012).
Her bridesmaids were half-sister Lady Frances, Zara Phillips (daughter of her first cousin Princess Anne), and Tara Noble-Singh, a family friend.



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
  AssignClass (5b7493ef-0f80-414f-9f24-29d4f03d8675)
 Call ID: 5b7493ef-0f80-414f-9f24-29d4f03d8675
  Args:
    source: Sarah_Chatto
    type: :Woman
  AssignClass (a0a2e3f9-2757-480e-8413-22c4aba25a8e)
 Call ID: a0a2e3f9-2757-480e-8413-22c4aba25a8e
  Args:
    source: Princess_Margaret
    type: :Woman
  AssignClass (e7b0eab4-e449-48f7-9c82-af856a41b788)
 Call ID: e7b0eab4-e449-48f7-9c82-af856a41b788
  Args:
    source: Antony_Armstrong-Jones
    type: :Man
  AssignClass (81224826-d620-4816-9edd-5b66724eda0c)
 Call ID: 81224826-d620-4816-9edd-5b66724eda0c
  Args:
    source: David_Armstrong-Jones
    type: :Man
  AssignClass (8c4b0957-c311-4a68-8c98-9be83afc7f8d)
 Call ID: 8c4b0957-c311-4a68-8c98-9be83afc7f8d
  Args:
    source: King_Charles_III
    type: :Man
  AssignClass (59f914f9-0e8e-424a-9c25-4c1a57d29246)
 Call ID: 59f914f9-0e8e-424a-9c25-4c1a57d29246
  Args:
    source: Daniel_Chatto
    type: :Man
  AssignClass (1144dd9f-b9ae-422b-84f8-ef14d692efe6)
 Call ID: 1144dd9f-b9ae-422b-84f8-ef14d692efe6
  Args:
    source: Tom_Chatto
    type: :Man
  AssignClass (777d8b93-7969-459c-a1b4-96a8d9a6971f)
 Call ID: 777d8b93-7969-459c-a1b4-96a8d9a6971f
  Args:
    source: Ros_Chatto
    type: :Woman
  AssignClass (129e4316-497a-4d48-970c-53bc0609cbf6)
 Call ID: 129e4316-497a-4d48-970c-53bc0609cbf6
  Args:
    source: Polly_Fry
    type: :Woman
  AssignClass (38e8d092-16cb-4d3b-a391-8d1ce316c121)
 Call ID: 38e8d092-16cb-4d3b-a391-8d1ce316c121
  Args:
    source: Lady_Frances_Armstrong-Jones
    type: :Woman
  AssignClass (3f1a51ff-3374-40bd-bb15-23a5e122ad79)
 Call ID: 3f1a51ff-3374-40bd-bb15-23a5e122ad79
  Args:
    source: Jasper_Cable-Alexander
    type: :Man
  AddLiteral (bdef1900-c082-4cda-850f-8ae16ec867da)
 Call ID: bdef1900-c082-4cda-850f-8ae16ec867da
  Args:
    literal_value: 1964
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Sarah_Chatto
  AddTriple (a6f08fc6-a69a-4cda-880f-f62b16a4b5cf)
 Call ID: a6f08fc6-a69a-4cda-880f-f62b16a4b5cf
  Args:
    relation: :hasMother
    source: Sarah_Chatto
    target: Princess_Margaret
  AddTriple (eecfca5e-3bbc-4fba-8ab7-d93ca7f435b2)
 Call ID: eecfca5e-3bbc-4fba-8ab7-d93ca7f435b2
  Args:
    target: Antony_Armstrong-Jones
    relation: :hasFather
    source: Sarah_Chatto
  AddTriple (ddb891b4-5b8b-4fdb-a8c4-bf19d843e5ac)
 Call ID: ddb891b4-5b8b-4fdb-a8c4-bf19d843e5ac
  Args:
    target: David_Armstrong-Jones
    relation: :hasBrother
    source: Sarah_Chatto
  AddTriple (2885ba39-5262-42c1-b371-f5d2090b1483)
 Call ID: 2885ba39-5262-42c1-b371-f5d2090b1483
  Args:
    relation: :hasFather
    source: David_Armstrong-Jones
    target: Antony_Armstrong-Jones
  AddTriple (ecfb0739-84e0-4d24-8617-22c12a3e6faa)
 Call ID: ecfb0739-84e0-4d24-8617-22c12a3e6faa
  Args:
    relation: :hasMother
    source: David_Armstrong-Jones
    target: Princess_Margaret
  AddTriple (1bd8afe2-3c07-4562-bfd4-310feff0740f)
 Call ID: 1bd8afe2-3c07-4562-bfd4-310feff0740f
  Args:
    relation: :hasFather
    source: Polly_Fry
    target: Antony_Armstrong-Jones
  AddTriple (85f55c63-d2a0-4272-a176-6c08d8776b68)
 Call ID: 85f55c63-d2a0-4272-a176-6c08d8776b68
  Args:
    relation: :hasFather
    source: Lady_Frances_Armstrong-Jones
    target: Antony_Armstrong-Jones
  AddTriple (70e1baf9-65fb-480f-8d24-be071f1d680a)
 Call ID: 70e1baf9-65fb-480f-8d24-be071f1d680a
  Args:
    relation: :hasFather
    source: Jasper_Cable-Alexander
    target: Antony_Armstrong-Jones
  AddTriple (47bf7e73-f3bb-492a-814b-161e6bee1de5)
 Call ID: 47bf7e73-f3bb-492a-814b-161e6bee1de5
  Args:
    target: Tom_Chatto
    source: Daniel_Chatto
    relation: :hasFather
  AddTriple (9f3e9d29-a314-440b-b5cb-2c1d43de9e50)
 Call ID: 9f3e9d29-a314-440b-b5cb-2c1d43de9e50
  Args:
    relation: :hasMother
    source: Daniel_Chatto
    target: Ros_Chatto
  AddLiteral (b89524f6-a7a6-4f3d-8d8e-97399b0f9321)
 Call ID: b89524f6-a7a6-4f3d-8d8e-97399b0f9321
  Args:
    relation: :hasBirthYear
    source: Tom_Chatto
    literal_type: xsd:integer
    literal_value: 1920
  AddLiteral (51aa591e-c9fa-47e3-8953-e8bb47637b3e)
 Call ID: 51aa591e-c9fa-47e3-8953-e8bb47637b3e
  Args:
    literal_value: 1982
    relation: :hasDeathYear
    source: Tom_Chatto
    literal_type: xsd:integer
  AddLiteral (3aa83cf1-5af8-4e30-8369-41cb6bb16154)
 Call ID: 3aa83cf1-5af8-4e30-8369-41cb6bb16154
  Args:
    source: Ros_Chatto
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2012
  AddLiteral (cc77276d-840d-41bb-9836-78bfb8938d0f)
 Call ID: cc77276d-840d-41bb-9836-78bfb8938d0f
  Args:
    literal_value: 1960
    relation: :hasBirthYear
    source: Polly_Fry
    literal_type: xsd:integer
  AddLiteral (e56a692d-5896-4136-9525-224cb5ca3f18)
 Call ID: e56a692d-5896-4136-9525-224cb5ca3f18
  Args:
    literal_value: 1979
    relation: :hasBirthYear
    source: Lady_Frances_Armstrong-Jones
    literal_type: xsd:integer
  AddLiteral (a8c05aec-505d-4b1b-ab42-b8ff992c8179)
 Call ID: a8c05aec-505d-4b1b-ab42-b8ff992c8179
  Args:
    source: Jasper_Cable-Alexander
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1998
  Finish (6f5c65ad-a61d-4363-8193-4ccc8fa3a0ef)
 Call ID: 6f5c65ad-a61d-4363-8193-4ccc8fa3a0ef
  Args: