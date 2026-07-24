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
The Dowager Princess Napoléon


Jean-Christophe, Prince Napoléon, Prince of Montfort (born Jean-Christophe Louis Ferdinand Albéric Napoléon Bonaparte; 11 July 1986), is a French businessman and the disputed head of the Imperial House of France, and as such the heir of Napoleon Bonaparte, the first Emperor of the French.
Family background

Jean-Christophe was born on 11 July 1986 in Saint-Raphaël, Var, France.
He is the son of Charles, Prince Napoléon and his first wife Princess Béatrice of Bourbon-Two Sicilies, daughter of the late Prince Ferdinand of Bourbon, Duke of Castro, a claimant to headship of the former Royal House of the Two Sicilies.
His parents divorced on 2 May 1989, two months before his third birthday.
Jean-Christophe is the great-great-great-grandnephew of Emperor Napoleon I (who has no legitimate direct descendants) through the emperor's youngest brother, Jérôme, King of Westphalia.
Through his mother, he is a descendant of King Louis XIV of France and through his great-grandmother, Princess Clémentine of Belgium, he descends from Leopold II of Belgium, William IV, Prince of Orange, Charles III of Spain, Frederick William I of Prussia, George II of Great Britain, Victor Emmanuel II, the first King of Italy, and Louis Philippe I, King of the French, who was the last king to rule France, while his great-great-grandfather was Prince Napoléon Bonaparte, the cousin of the Emperor Napoleon III, France's most recent monarch.
Prince Napoléon

Jean-Christophe's grandfather, Louis, Prince Napoléon, died in 1997 and stipulated in his will that he wished his 11-year-old grandson Jean-Christophe to succeed him as Head of the Imperial House of France rather than the boy's father, Charles, who had embraced republican principles and decided to remarry without his father's consent.
Despite the dynastic dispute, Jean-Christophe's father has stated that "there will never be conflict" between him and his son over the imperial succession.
Education and career

Jean-Christophe studied at Lycée Saint-Dominique in Neuilly-sur-Seine from 2001 to 2004, obtaining a baccalauréat with honours in the sciences and mathematics.
Jean-Christophe and Olympia have one son, Prince Louis Charles Riprand Victor Jérôme Marie Napoléon, born 7 December 2022 in Paris.



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
  AssignClass (17043808-f680-48e6-bce8-448542437569)
 Call ID: 17043808-f680-48e6-bce8-448542437569
  Args:
    type: :Person
    source: Jean-Christophe_Prince_Napoléon
  AssignClass (0cbe9dbb-0908-4b61-a000-e1925d2de8b3)
 Call ID: 0cbe9dbb-0908-4b61-a000-e1925d2de8b3
  Args:
    type: :Man
    source: Jean-Christophe_Prince_Napoléon
  AddLiteral (82919f25-5a72-4768-977f-b798b4ed547c)
 Call ID: 82919f25-5a72-4768-977f-b798b4ed547c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1986
    source: Jean-Christophe_Prince_Napoléon
  AssignClass (ac79eca9-0141-4868-b19b-b390dc777c72)
 Call ID: ac79eca9-0141-4868-b19b-b390dc777c72
  Args:
    type: :Person
    source: Charles_Prince_Napoléon
  AssignClass (fd069ce1-b7b6-4c2d-a7bf-52234d6e32e7)
 Call ID: fd069ce1-b7b6-4c2d-a7bf-52234d6e32e7
  Args:
    type: :Man
    source: Charles_Prince_Napoléon
  AssignClass (8bfc985d-7cd2-4cdd-bbd6-5c3a85c6adfb)
 Call ID: 8bfc985d-7cd2-4cdd-bbd6-5c3a85c6adfb
  Args:
    type: :Person
    source: Princess_Béatrice_of_Bourbon-Two_Sicilies
  AssignClass (dfcbb466-4fbc-416c-a77e-d38c32957d05)
 Call ID: dfcbb466-4fbc-416c-a77e-d38c32957d05
  Args:
    type: :Woman
    source: Princess_Béatrice_of_Bourbon-Two_Sicilies
  AddTriple (29eb5f6d-a8a5-425d-aecd-5b8b8f70b140)
 Call ID: 29eb5f6d-a8a5-425d-aecd-5b8b8f70b140
  Args:
    source: Jean-Christophe_Prince_Napoléon
    target: Charles_Prince_Napoléon
    relation: :hasFather
  AddTriple (81b4fcbd-18ec-49b1-8f64-ff7845910a2f)
 Call ID: 81b4fcbd-18ec-49b1-8f64-ff7845910a2f
  Args:
    source: Jean-Christophe_Prince_Napoléon
    target: Princess_Béatrice_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AssignClass (bf1d8fcf-9685-4395-a29f-6b7d629a1155)
 Call ID: bf1d8fcf-9685-4395-a29f-6b7d629a1155
  Args:
    type: :Person
    source: Prince_Ferdinand_of_Bourbon_Duke_of_Castro
  AssignClass (ed494273-0222-4791-a88e-44a9d4d878c8)
 Call ID: ed494273-0222-4791-a88e-44a9d4d878c8
  Args:
    type: :Man
    source: Prince_Ferdinand_of_Bourbon_Duke_of_Castro
  AddTriple (85f82109-7924-4035-bf86-11b5f20c005c)
 Call ID: 85f82109-7924-4035-bf86-11b5f20c005c
  Args:
    relation: :hasFather
    source: Princess_Béatrice_of_Bourbon-Two_Sicilies
    target: Prince_Ferdinand_of_Bourbon_Duke_of_Castro
  AssignClass (1d0d4cab-6f5c-4602-bafd-a8f51b5b9c61)
 Call ID: 1d0d4cab-6f5c-4602-bafd-a8f51b5b9c61
  Args:
    type: :Person
    source: Louis_Prince_Napoléon
  AssignClass (6107d3c0-50a2-40b1-9373-f0d50e7fd111)
 Call ID: 6107d3c0-50a2-40b1-9373-f0d50e7fd111
  Args:
    type: :Man
    source: Louis_Prince_Napoléon
  AddLiteral (9e4d0748-2485-4c0a-8c72-cf549a37a6e2)
 Call ID: 9e4d0748-2485-4c0a-8c72-cf549a37a6e2
  Args:
    source: Louis_Prince_Napoléon
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1997
  AddTriple (a2d047c4-00d3-468d-9fb3-fa6d4bc0d5a8)
 Call ID: a2d047c4-00d3-468d-9fb3-fa6d4bc0d5a8
  Args:
    source: Charles_Prince_Napoléon
    target: Louis_Prince_Napoléon
    relation: :hasFather
  AssignClass (f7e83a7c-f2f0-470b-a523-d90eb4d7c91a)
 Call ID: f7e83a7c-f2f0-470b-a523-d90eb4d7c91a
  Args:
    type: :Person
    source: Olympia
  AssignClass (9f03b8c8-fc0f-4321-a186-f1059cb0b7cf)
 Call ID: 9f03b8c8-fc0f-4321-a186-f1059cb0b7cf
  Args:
    type: :Woman
    source: Olympia
  AssignClass (44414a0c-b145-4d2b-91a1-de6675e6c980)
 Call ID: 44414a0c-b145-4d2b-91a1-de6675e6c980
  Args:
    type: :Person
    source: Prince_Louis_Charles_Riprand_Victor_Jérôme_Marie_Napoléon
  AssignClass (92bac41a-d357-495a-a091-954db86dbcc5)
 Call ID: 92bac41a-d357-495a-a091-954db86dbcc5
  Args:
    type: :Man
    source: Prince_Louis_Charles_Riprand_Victor_Jérôme_Marie_Napoléon
  AddLiteral (71aefc83-df59-4f19-b8b1-1ebc739b700b)
 Call ID: 71aefc83-df59-4f19-b8b1-1ebc739b700b
  Args:
    source: Prince_Louis_Charles_Riprand_Victor_Jérôme_Marie_Napoléon
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2022
  AddTriple (0ee4d600-9f67-47d5-9ca9-5cf85031de12)
 Call ID: 0ee4d600-9f67-47d5-9ca9-5cf85031de12
  Args:
    source: Prince_Louis_Charles_Riprand_Victor_Jérôme_Marie_Napoléon
    target: Jean-Christophe_Prince_Napoléon
    relation: :hasFather
  AddTriple (c7b229af-e1b7-4b28-8f63-c8b1899e7b2e)
 Call ID: c7b229af-e1b7-4b28-8f63-c8b1899e7b2e
  Args:
    relation: :hasMother
    target: Olympia
    source: Prince_Louis_Charles_Riprand_Victor_Jérôme_Marie_Napoléon
  Finish (bad65f40-8ead-443d-8549-5cf59ebfb295)
 Call ID: bad65f40-8ead-443d-8549-5cf59ebfb295
  Args: