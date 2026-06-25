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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Bernhard Lucas Emmanuel of Orange-Nassau, van Vollenhoven (born 25 December 1969) is a Dutch racing driver, entrepreneur and member of the Dutch royal family.
He is the second son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
With Willem-Alexander's succession however, he is no longer a member of the Dutch Royal House, and is no longer in line to direct succession to the Dutch throne, but still retains his membership of the Dutch royal family 


Early life and education

Bernhard was born on 25 December 1969 in Nijmegen in the Netherlands.
He is the second son of Princess Margriet and Pieter van Vollenhoven.
He has three brothers: Princes Maurits, Pieter-Christiaan, and Floris.
Subsequently, in 1989 he attended Groningen University in the Netherlands where he studied marketing and market research.
Business

Bernhard is a self-employed entrepreneur.
In 2002, the name Ritzen Koeriers was changed to Logistieke Meesters, at which time Bernhard was no longer involved in the business.
Marriage and family

While studying in Groningen, Bernhard met Annette Sekrève, (born 18 April 1972).
They have three children: Isabella Lily Juliana (born 2002), Samuel Bernhard Louis (born 2004), and Benjamin Pieter Floris (born 2008).
According to a royal decree of 5 July 2000, the children were granted the family name van Vollenhoven, without titles.
In January 2026, Bernhard and Annette announced that they were to divorce.
Upon the announcement of the planned abdication of Queen Beatrix, which took place on 30 April 2013, it was also restated that after the abdication, the children of Princess Margriet and Pieter van Vollenhoven would no longer be eligible for the throne.
Health

Bernhard has been receiving treatment for Crohn's disease since 2002.
Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (bcc99ab1-cf4a-4230-a83a-8460a7611847)
 Call ID: bcc99ab1-cf4a-4230-a83a-8460a7611847
  Args:
    type: :Woman
    source: :Beatrix
  AssignClass (54852f0d-c7b6-437e-9e16-74f0bc8b2d70)
 Call ID: 54852f0d-c7b6-437e-9e16-74f0bc8b2d70
  Args:
    type: :Woman
    source: :Margriet
  AssignClass (613bdc75-121c-4eb8-99f5-415782d11f08)
 Call ID: 613bdc75-121c-4eb8-99f5-415782d11f08
  Args:
    source: :Pieter_van_Vollenhoven
    type: :Man
  AssignClass (b357f2b5-0b7f-44d3-9a7a-a8fdbd2d9001)
 Call ID: b357f2b5-0b7f-44d3-9a7a-a8fdbd2d9001
  Args:
    source: :Bernhard_van_Vollenhoven
    type: :Man
  AddLiteral (adf91522-a2c3-46ca-9c88-3d08789b305a)
 Call ID: adf91522-a2c3-46ca-9c88-3d08789b305a
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1969
    source: :Bernhard_van_Vollenhoven
  AddTriple (043882a5-8821-4400-80ce-eeda8ae69849)
 Call ID: 043882a5-8821-4400-80ce-eeda8ae69849
  Args:
    relation: :hasMother
    target: :Margriet
    source: :Bernhard_van_Vollenhoven
  AddTriple (a6d021e2-2ee3-4554-af13-93b243d8b8a1)
 Call ID: a6d021e2-2ee3-4554-af13-93b243d8b8a1
  Args:
    relation: :hasFather
    target: :Pieter_van_Vollenhoven
    source: :Bernhard_van_Vollenhoven
  AssignClass (88c46f02-5ce4-4357-93c3-2dab3ec2cc74)
 Call ID: 88c46f02-5ce4-4357-93c3-2dab3ec2cc74
  Args:
    source: :Maurits_van_Vollenhoven
    type: :Man
  AssignClass (53ca6475-b039-4fb2-8dac-833ad2f73ae5)
 Call ID: 53ca6475-b039-4fb2-8dac-833ad2f73ae5
  Args:
    type: :Man
    source: :Pieter-Christiaan_van_Vollenhoven
  AssignClass (900fb622-4e80-47bc-abe9-7aab61b1cc45)
 Call ID: 900fb622-4e80-47bc-abe9-7aab61b1cc45
  Args:
    source: :Floris_van_Vollenhoven
    type: :Man
  AddTriple (10a92e90-9f25-4065-895d-bb22e32fa87a)
 Call ID: 10a92e90-9f25-4065-895d-bb22e32fa87a
  Args:
    source: :Bernhard_van_Vollenhoven
    target: :Maurits_van_Vollenhoven
    relation: :isBrotherOf
  AddTriple (d130450a-fc2d-4bb8-ad5e-41cf5d502fe2)
 Call ID: d130450a-fc2d-4bb8-ad5e-41cf5d502fe2
  Args:
    relation: :isBrotherOf
    target: :Pieter-Christiaan_van_Vollenhoven
    source: :Bernhard_van_Vollenhoven
  AddTriple (1d113bde-66ae-4ef0-8788-5028e72ec922)
 Call ID: 1d113bde-66ae-4ef0-8788-5028e72ec922
  Args:
    source: :Bernhard_van_Vollenhoven
    relation: :isBrotherOf
    target: :Floris_van_Vollenhoven
  AssignClass (33a7e5a1-12c6-4932-b6f7-24f2b41809f7)
 Call ID: 33a7e5a1-12c6-4932-b6f7-24f2b41809f7
  Args:
    source: :Annette_Sekreve
    type: :Woman
  AddLiteral (ea6ac5b4-2171-40d9-bb13-39e19a389557)
 Call ID: ea6ac5b4-2171-40d9-bb13-39e19a389557
  Args:
    relation: :hasBirthYear
    source: :Annette_Sekreve
    literal_value: 1972
    literal_type: xsd:integer
  AssignClass (b7951920-0425-4fe2-bc4a-1dabed49b654)
 Call ID: b7951920-0425-4fe2-bc4a-1dabed49b654
  Args:
    type: :Woman
    source: :Isabella_Lily_Juliana_van_Vollenhoven
  AssignClass (d102640a-b8ca-4553-8895-c16f9e05cb73)
 Call ID: d102640a-b8ca-4553-8895-c16f9e05cb73
  Args:
    type: :Man
    source: :Samuel_Bernhard_Louis_van_Vollenhoven
  AssignClass (ac1fbf5b-60e2-41ac-959e-9726a7aeb403)
 Call ID: ac1fbf5b-60e2-41ac-959e-9726a7aeb403
  Args:
    source: :Benjamin_Pieter_Floris_van_Vollenhoven
    type: :Man
  AddTriple (f3ef1a8c-9246-415b-8039-7d1c49ad59d8)
 Call ID: f3ef1a8c-9246-415b-8039-7d1c49ad59d8
  Args:
    target: :Annette_Sekreve
    relation: :hasMother
    source: :Isabella_Lily_Juliana_van_Vollenhoven
  AddTriple (d0ac4e0f-3a7e-456b-b194-8e572d4d0e0c)
 Call ID: d0ac4e0f-3a7e-456b-b194-8e572d4d0e0c
  Args:
    source: :Isabella_Lily_Juliana_van_Vollenhoven
    target: :Bernhard_van_Vollenhoven
    relation: :hasFather
  AddTriple (ad787d12-c9c6-4d6c-810c-632f88029f36)
 Call ID: ad787d12-c9c6-4d6c-810c-632f88029f36
  Args:
    source: :Samuel_Bernhard_Louis_van_Vollenhoven
    target: :Annette_Sekreve
    relation: :hasMother
  AddTriple (77c3e667-d596-462e-885e-ee6fa2d32d58)
 Call ID: 77c3e667-d596-462e-885e-ee6fa2d32d58
  Args:
    relation: :hasFather
    target: :Bernhard_van_Vollenhoven
    source: :Samuel_Bernhard_Louis_van_Vollenhoven
  AddTriple (6c310a1d-5926-498e-be11-5c3b4432ed4b)
 Call ID: 6c310a1d-5926-498e-be11-5c3b4432ed4b
  Args:
    source: :Benjamin_Pieter_Floris_van_Vollenhoven
    relation: :hasMother
    target: :Annette_Sekreve
  AddTriple (561a3fd4-687c-4a5d-959c-2c211b7e67ad)
 Call ID: 561a3fd4-687c-4a5d-959c-2c211b7e67ad
  Args:
    target: :Bernhard_van_Vollenhoven
    relation: :hasFather
    source: :Benjamin_Pieter_Floris_van_Vollenhoven
  Finish (78bb9a6d-d262-440b-9af0-8d9f919e024e)
 Call ID: 78bb9a6d-d262-440b-9af0-8d9f919e024e
  Args: