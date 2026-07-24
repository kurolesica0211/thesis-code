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
Berthold Prinz und Markgraf von Baden (24 February 1906 – 27 October 1963), styled Margrave of Baden and Duke of Zähringen, was the head of the House of Baden, which had reigned over the Grand Duchy of Baden until 1918, from 1929 until his death.
He was the brother-in-law of Prince Philip, Duke of Edinburgh, through his marriage to Philip's sister, Princess Theodora of Greece and Denmark.
Marriage and children

The only son and younger child of Prince Maximilian, Margrave of Baden and Princess Marie Louise of Hanover, Berthold married his second cousin Princess Theodora of Greece and Denmark, daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, on 17 August 1931 in Baden-Baden.
Via his marriage, he was the brother-in-law of Prince Philip of Greece and Denmark, later Prince Philip, Duke of Edinburgh from November 1947.
His bride was also his second cousin, through Christian IX of Denmark.
The couple had three children:


Personal life

He was conscripted as a soldier into the army of the Wehrmacht, but served only briefly and was exempted from military service in 1940 after being injured in France.
Death

Berthold died on 27 October 1963, aged 57, in Spaichingen.
He was succeeded as titular margrave and head of house by his son Max.



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
  AssignClass (86b1578a-dd11-4091-acf6-f8e82818a85f)
 Call ID: 86b1578a-dd11-4091-acf6-f8e82818a85f
  Args:
    source: :Berthold_Prinz_und_Markgraf_von_Baden
    type: :Man
  AssignClass (2ba391e5-85df-4969-8a46-2ec2ee779953)
 Call ID: 2ba391e5-85df-4969-8a46-2ec2ee779953
  Args:
    type: :Person
    source: :Berthold_Prinz_und_Markgraf_von_Baden
  AddLiteral (51eabfc3-69c6-4b39-a71e-352f13bf72d8)
 Call ID: 51eabfc3-69c6-4b39-a71e-352f13bf72d8
  Args:
    source: :Berthold_Prinz_und_Markgraf_von_Baden
    literal_type: xsd:positiveInteger
    literal_value: 1906
    relation: :hasBirthYear
  AddLiteral (b865004d-f383-41c2-a7de-bcf6cc3e5918)
 Call ID: b865004d-f383-41c2-a7de-bcf6cc3e5918
  Args:
    literal_value: 1963
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
    source: :Berthold_Prinz_und_Markgraf_von_Baden
  AssignClass (64f5b30b-010a-4f9e-bde0-f9e394b5cb32)
 Call ID: 64f5b30b-010a-4f9e-bde0-f9e394b5cb32
  Args:
    source: :Prince_Maximilian_Margrave_of_Baden
    type: :Man
  AssignClass (cc551084-cac1-4fd7-bd56-0908ceb24c0f)
 Call ID: cc551084-cac1-4fd7-bd56-0908ceb24c0f
  Args:
    source: :Prince_Maximilian_Margrave_of_Baden
    type: :Person
  AssignClass (d3625caa-22e1-4c41-9878-03eab112d171)
 Call ID: d3625caa-22e1-4c41-9878-03eab112d171
  Args:
    type: :Woman
    source: :Princess_Marie_Louise_of_Hanover
  AssignClass (df25d8b5-b17a-4954-8e70-9f5480970dcc)
 Call ID: df25d8b5-b17a-4954-8e70-9f5480970dcc
  Args:
    type: :Person
    source: :Princess_Marie_Louise_of_Hanover
  AddTriple (a47fc1ad-c014-4776-8777-927fed15596f)
 Call ID: a47fc1ad-c014-4776-8777-927fed15596f
  Args:
    source: :Berthold_Prinz_und_Markgraf_von_Baden
    relation: :hasFather
    target: :Prince_Maximilian_Margrave_of_Baden
  AddTriple (1d3bf151-d8c4-4401-8620-466a6578991f)
 Call ID: 1d3bf151-d8c4-4401-8620-466a6578991f
  Args:
    relation: :hasMother
    target: :Princess_Marie_Louise_of_Hanover
    source: :Berthold_Prinz_und_Markgraf_von_Baden
  AssignClass (23287cd7-542f-4142-89f3-4ea922305a7b)
 Call ID: 23287cd7-542f-4142-89f3-4ea922305a7b
  Args:
    source: :Princess_Theodora_of_Greece_and_Denmark
    type: :Woman
  AssignClass (ef13b554-156e-433e-aa4c-1700c65250d2)
 Call ID: ef13b554-156e-433e-aa4c-1700c65250d2
  Args:
    type: :Person
    source: :Princess_Theodora_of_Greece_and_Denmark
  AddLiteral (6945bc45-2456-4ebc-a467-13b2f3e00c5e)
 Call ID: 6945bc45-2456-4ebc-a467-13b2f3e00c5e
  Args:
    literal_value: 1931
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
    source: :Berthold_Prinz_und_Markgraf_von_Baden
  AddTriple (5b5f68a4-0096-4c62-86a2-9e3a44f45325)
 Call ID: 5b5f68a4-0096-4c62-86a2-9e3a44f45325
  Args:
    source: :Berthold_Prinz_und_Markgraf_von_Baden
    relation: :hasRelation
    target: :Princess_Theodora_of_Greece_and_Denmark
  AssignClass (cf7a3e29-5f69-4e6b-8bfc-6b0233db27fd)
 Call ID: cf7a3e29-5f69-4e6b-8bfc-6b0233db27fd
  Args:
    type: :Man
    source: :Prince_Andrew_of_Greece_and_Denmark
  AssignClass (86467f47-0e6c-479b-bc48-2bb993b53eee)
 Call ID: 86467f47-0e6c-479b-bc48-2bb993b53eee
  Args:
    source: :Prince_Andrew_of_Greece_and_Denmark
    type: :Person
  AssignClass (d7701ae1-3bef-4ac1-b7fc-e244abaf3f19)
 Call ID: d7701ae1-3bef-4ac1-b7fc-e244abaf3f19
  Args:
    type: :Woman
    source: :Princess_Alice_of_Battenberg
  AssignClass (ad99947d-c291-42f2-af6f-616df4941fcb)
 Call ID: ad99947d-c291-42f2-af6f-616df4941fcb
  Args:
    type: :Person
    source: :Princess_Alice_of_Battenberg
  AddTriple (f3396355-303d-44b7-9d42-cdbe252b211c)
 Call ID: f3396355-303d-44b7-9d42-cdbe252b211c
  Args:
    relation: :hasFather
    target: :Prince_Andrew_of_Greece_and_Denmark
    source: :Princess_Theodora_of_Greece_and_Denmark
  AddTriple (8823515a-ff22-4f8d-8962-cb9029571981)
 Call ID: 8823515a-ff22-4f8d-8962-cb9029571981
  Args:
    target: :Princess_Alice_of_Battenberg
    relation: :hasMother
    source: :Princess_Theodora_of_Greece_and_Denmark
  AssignClass (a8f4a45a-9e2c-4164-b787-153b36ccbb73)
 Call ID: a8f4a45a-9e2c-4164-b787-153b36ccbb73
  Args:
    source: :Prince_Philip_Duke_of_Edinburgh
    type: :Man
  AssignClass (805eb845-08f8-47b7-9a78-3d29f4f91f75)
 Call ID: 805eb845-08f8-47b7-9a78-3d29f4f91f75
  Args:
    type: :Person
    source: :Prince_Philip_Duke_of_Edinburgh
  AddTriple (de8b7415-4911-4e0e-a55d-57841c49fcef)
 Call ID: de8b7415-4911-4e0e-a55d-57841c49fcef
  Args:
    target: :Prince_Philip_Duke_of_Edinburgh
    relation: :isSisterOf
    source: :Princess_Theodora_of_Greece_and_Denmark
  AssignClass (5809132e-1bb8-44ed-ba6f-2ce2f36d176b)
 Call ID: 5809132e-1bb8-44ed-ba6f-2ce2f36d176b
  Args:
    type: :Man
    source: :Max
  AssignClass (8927a778-67f0-4416-a151-f07645e71222)
 Call ID: 8927a778-67f0-4416-a151-f07645e71222
  Args:
    type: :Person
    source: :Max
  AddTriple (6d2d4dfb-a61f-4f86-a755-7b3bef896718)
 Call ID: 6d2d4dfb-a61f-4f86-a755-7b3bef896718
  Args:
    relation: :hasSon
    target: :Max
    source: :Berthold_Prinz_und_Markgraf_von_Baden
  Finish (1602f0bd-8500-41ed-91d0-93c54f81a1cd)
 Call ID: 1602f0bd-8500-41ed-91d0-93c54f81a1cd
  Args: