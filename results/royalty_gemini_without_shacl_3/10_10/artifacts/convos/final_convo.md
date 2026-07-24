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
Princess Cecilie of Prussia (Cecilie Viktoria Anastasia Zita Thyra Adelheid; 5 September 1917 – 21 April 1975) was a member of the House of Hohenzollern.
She was the younger daughter and sixth child of Wilhelm, German Crown Prince, and Duchess Cecilie of Mecklenburg-Schwerin.
Early life

Cecilie was born on 5 September 1917 at Cecilienhof Palace in Potsdam, which had only been completed weeks prior to her birth, during World War I and the reign of paternal grandfather, Wilhelm II, as German Emperor and King of Prussia.
One year after her birth, on 9 November 1918, her grandfather and other German monarchs abdicated and the German Empire was abolished.
Cecilienhof was returned to Cecilie's family in 1926.
During World War II, Cecilie worked at a pharmacy in Potsdam and trained as a nurse with the German Red Cross.
As the Red Army descended on Potsdam at the end of the war, Cecilie was sent to live with Hessian relatives at Schloss Wolfsgarten.
There, she met American Captain Clyde Kenneth Harris, a member of the Monuments, Fine Arts, and Archives Unit who was investigating the Darmstadt Madonna for her cousin, Ludwig, Prince of Hesse and by Rhine.
Prince Vsevolod of Russia proposed to her twice, but she declined both times.
Marriage and family

Cecilie and Harris were married on 21 June 1949 at Hohenzollern Castle.
They had one daughter, Kira Alexandrine Brigid Cecilie Ingrid Harris (born 20 October 1954) who married John Mitchell Johnson (12 May 1951 Dallas, Texas-) and had one son, Philip Louis Johnson (18 Oct 1985 Fort Worth, Texas-).
While visiting family in Germany, Cecilie died in Königstein im Taunus on 21 April 1975, aged 57.



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
  AssignClass (9afc50cb-8e72-4d70-81fb-a0feba561a00)
 Call ID: 9afc50cb-8e72-4d70-81fb-a0feba561a00
  Args:
    type: :Woman
    source: Princess_Cecilie_of_Prussia
  AssignClass (c54733d0-97e1-413d-8cb2-5b91402aed11)
 Call ID: c54733d0-97e1-413d-8cb2-5b91402aed11
  Args:
    type: :Person
    source: Princess_Cecilie_of_Prussia
  AddLiteral (4fff137d-38ac-4c67-a90a-25a478dfccd3)
 Call ID: 4fff137d-38ac-4c67-a90a-25a478dfccd3
  Args:
    literal_type: xsd:integer
    literal_value: 1917
    relation: :hasBirthYear
    source: Princess_Cecilie_of_Prussia
  AddLiteral (09806684-b4e4-4d45-b5ac-7247e3bb990c)
 Call ID: 09806684-b4e4-4d45-b5ac-7247e3bb990c
  Args:
    literal_value: 1975
    source: Princess_Cecilie_of_Prussia
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (30ff90ae-022e-4dab-92c4-84d1471d4c98)
 Call ID: 30ff90ae-022e-4dab-92c4-84d1471d4c98
  Args:
    type: :Man
    source: Wilhelm_German_Crown_Prince
  AssignClass (330cc821-3f1f-447f-a57a-3b16ab75a891)
 Call ID: 330cc821-3f1f-447f-a57a-3b16ab75a891
  Args:
    type: :Person
    source: Wilhelm_German_Crown_Prince
  AssignClass (205ae104-76a8-44e1-a7fc-18ebeae11c3c)
 Call ID: 205ae104-76a8-44e1-a7fc-18ebeae11c3c
  Args:
    type: :Woman
    source: Duchess_Cecilie_of_Mecklenburg-Schwerin
  AssignClass (30e788b5-0858-4605-8c23-f55f54c4445f)
 Call ID: 30e788b5-0858-4605-8c23-f55f54c4445f
  Args:
    type: :Person
    source: Duchess_Cecilie_of_Mecklenburg-Schwerin
  AddTriple (b5d212d2-db35-439d-8de7-2f02046444dc)
 Call ID: b5d212d2-db35-439d-8de7-2f02046444dc
  Args:
    target: Wilhelm_German_Crown_Prince
    source: Princess_Cecilie_of_Prussia
    relation: :hasFather
  AddTriple (135fe530-d4f6-4248-8fb1-d1bcedd24358)
 Call ID: 135fe530-d4f6-4248-8fb1-d1bcedd24358
  Args:
    relation: :hasMother
    source: Princess_Cecilie_of_Prussia
    target: Duchess_Cecilie_of_Mecklenburg-Schwerin
  AssignClass (739d3a39-2e36-43f4-bf54-0f0c9f8164cd)
 Call ID: 739d3a39-2e36-43f4-bf54-0f0c9f8164cd
  Args:
    type: :Man
    source: Clyde_Kenneth_Harris
  AssignClass (a38a01ae-9a29-4ea3-83c4-2991eab717a2)
 Call ID: a38a01ae-9a29-4ea3-83c4-2991eab717a2
  Args:
    type: :Person
    source: Clyde_Kenneth_Harris
  AddTriple (5aa1c17e-53d7-43c1-ad6e-a1386c1f4c36)
 Call ID: 5aa1c17e-53d7-43c1-ad6e-a1386c1f4c36
  Args:
    target: Clyde_Kenneth_Harris
    source: Princess_Cecilie_of_Prussia
    relation: :hasRelation
  AddLiteral (75977877-a1a4-4941-8c34-d14af6bdf3f3)
 Call ID: 75977877-a1a4-4941-8c34-d14af6bdf3f3
  Args:
    literal_value: 1949
    source: Princess_Cecilie_of_Prussia
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (56c73344-2679-467f-8d93-670241e22453)
 Call ID: 56c73344-2679-467f-8d93-670241e22453
  Args:
    type: :Woman
    source: Kira_Alexandrine_Brigid_Cecilie_Ingrid_Harris
  AssignClass (f17ea03e-ac6d-491e-892a-8ead68cbf8dc)
 Call ID: f17ea03e-ac6d-491e-892a-8ead68cbf8dc
  Args:
    type: :Person
    source: Kira_Alexandrine_Brigid_Cecilie_Ingrid_Harris
  AddTriple (49bced19-a6c1-498f-a820-e1255efb07bd)
 Call ID: 49bced19-a6c1-498f-a820-e1255efb07bd
  Args:
    relation: :hasMother
    source: Kira_Alexandrine_Brigid_Cecilie_Ingrid_Harris
    target: Princess_Cecilie_of_Prussia
  AddTriple (cd9eccce-4c15-4fc9-9fe2-77b5f51882c3)
 Call ID: cd9eccce-4c15-4fc9-9fe2-77b5f51882c3
  Args:
    source: Kira_Alexandrine_Brigid_Cecilie_Ingrid_Harris
    relation: :hasFather
    target: Clyde_Kenneth_Harris
  AssignClass (73bfc485-c7f8-4768-a018-c711ecbb5689)
 Call ID: 73bfc485-c7f8-4768-a018-c711ecbb5689
  Args:
    type: :Man
    source: John_Mitchell_Johnson
  AssignClass (2c289aa6-6ea7-4280-9f23-f4146b433dee)
 Call ID: 2c289aa6-6ea7-4280-9f23-f4146b433dee
  Args:
    type: :Person
    source: John_Mitchell_Johnson
  AddTriple (6d3a19a9-d40f-4b4b-aeb1-c178bd1804dc)
 Call ID: 6d3a19a9-d40f-4b4b-aeb1-c178bd1804dc
  Args:
    target: John_Mitchell_Johnson
    source: Kira_Alexandrine_Brigid_Cecilie_Ingrid_Harris
    relation: :hasRelation
  AssignClass (5d78de46-fb80-49c7-8d34-1f33930038d9)
 Call ID: 5d78de46-fb80-49c7-8d34-1f33930038d9
  Args:
    type: :Man
    source: Philip_Louis_Johnson
  AssignClass (4e473870-a387-4003-8d3c-f14224c0bb44)
 Call ID: 4e473870-a387-4003-8d3c-f14224c0bb44
  Args:
    type: :Person
    source: Philip_Louis_Johnson
  AddTriple (c27cb93b-86d5-4159-b343-19015d6c25aa)
 Call ID: c27cb93b-86d5-4159-b343-19015d6c25aa
  Args:
    target: John_Mitchell_Johnson
    relation: :hasFather
    source: Philip_Louis_Johnson
  AddTriple (312b6157-e704-4ab3-8423-92532c888c76)
 Call ID: 312b6157-e704-4ab3-8423-92532c888c76
  Args:
    source: Philip_Louis_Johnson
    relation: :hasMother
    target: Kira_Alexandrine_Brigid_Cecilie_Ingrid_Harris
  Finish (067a2426-bf10-4d9f-9d29-51f98814575c)
 Call ID: 067a2426-bf10-4d9f-9d29-51f98814575c
  Args: