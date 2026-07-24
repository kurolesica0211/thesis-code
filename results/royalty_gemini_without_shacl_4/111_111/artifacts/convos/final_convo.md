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
India Amanda Caroline Hicks (born 5 September 1967) is a British designer, writer, businesswoman and former fashion model.
After graduating from the New England School of Photography, Hicks became an interior designer and a model for Ralph Lauren, among others.
Hicks travels frequently to disaster sites in her role with the non-profit organisation Global Empowerment Mission.
A daughter of Lady Pamela Hicks, she is a maternal descendant of the House of Mountbatten and a relative of the British royal family.
Early life

India Amanda Caroline Hicks was born on 5 September 1967 in Lambeth, London.
Hicks is the third child of Lady Pamela Mountbatten and David Nightingale Hicks.
Her mother was a lady-in-waiting to Queen Elizabeth II and her father was a famous interior designer.
She is the granddaughter of the 1st Earl and Countess Mountbatten of Burma and the second cousin and goddaughter of Charles III.
Hicks grew up in Oxfordshire, England.
Hicks was exposed to design at an early age through her father and brother, who were both architects.
The 11-year-old Hicks was on holiday in Ireland in 1979 when her grandfather was killed by a bomb planted on his boat.
In 1981, she served as bridesmaid to Lady Diana Spencer at her wedding to Prince Charles.
Hicks went to boarding school in Scotland at Gordonstoun, from which she was expelled for having boys in her room.
She then backpacked across India.
Hicks moved to Boston, Massachusetts at age 18 to study photography at the New England School of Photography, where she graduated in 1990.
Career

After graduating college, Hicks' father introduced her to Emilio Pucci in Florence, Italy, where she modelled swimsuits.
Hicks moved to the Bahamas in 1996.
In the Bahamas, Hicks restored homes, invested and remodelled a hotel, and published several books on design and lifestyle.
Hicks also started a boutique shop in the Bahamas called the Sugar Mill Trading Company with business partner Linda Griffin.
From 2005 to 2014, Hicks worked with Crabtree & Evelyn as a spokeswoman and creative consultant for home and skincare products.
The company created the India Hicks Island Living and India Hicks Island Night lines of soaps, candles, and perfumes.
In 2008, Hicks co-hosted the second season of the Bravo interior design show Top Design in Los Angeles, California.
Hicks also became a public commentator on events surrounding the royal family and the 2011 wedding of Prince William and Catherine Middleton.
In 2015, Hicks created an e-commerce venture called India Hicks Inc. with partners Nicholas Keuper and HauteLook.
Hicks also worked with the Home Shopping Network on a line of bedding products called India Hicks Island Living.
Personal life

Hicks met her husband David Flint Wood as a child.
He was previously in a relationship with her cousin, Lady Helen Windsor and then Susannah Constantine, a fashion journalist and the former girlfriend of her other cousin, David Armstrong-Jones, 2nd Earl of Snowdon.
India and David re-connected as adults during a holiday in the Bahamas.
The couple have a house, "America Farm" in Ewelme, Oxfordshire, built on land that Hicks had inherited and replacing two redundant farm workers' cottages.
Hicks' book about the project, India Hicks:
Hicks has competed in several marathons.
In 2020, Hicks pleaded guilty at Uxbridge Magistrates' Court to shoplifting a coat and was ordered to pay costs and a victim surcharge.
Her spokesperson stated: "The court accepted that at the time of taking the coat, India had simply been absent-minded and hadn't intended to leave without paying for it".



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (7f0a9ceb-5330-49ba-b992-c174c5e5be7c)
 Call ID: 7f0a9ceb-5330-49ba-b992-c174c5e5be7c
  Args:
    type: :Woman
    source: India_Hicks
  AssignClass (efc1c014-e7cf-4aa7-9780-181232d82a10)
 Call ID: efc1c014-e7cf-4aa7-9780-181232d82a10
  Args:
    type: :Person
    source: India_Hicks
  AddLiteral (eacf6ac0-45ec-4354-a87c-c787b646795e)
 Call ID: eacf6ac0-45ec-4354-a87c-c787b646795e
  Args:
    literal_value: 1967
    source: India_Hicks
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (ea1e7847-dd75-410c-bbb3-3c6e741c1554)
 Call ID: ea1e7847-dd75-410c-bbb3-3c6e741c1554
  Args:
    type: :Woman
    source: Lady_Pamela_Mountbatten
  AssignClass (4d599019-ab2a-45c6-96ea-b1729b212b22)
 Call ID: 4d599019-ab2a-45c6-96ea-b1729b212b22
  Args:
    type: :Person
    source: Lady_Pamela_Mountbatten
  AssignClass (abe30e8f-9740-4c97-9b08-1eeac97fd98b)
 Call ID: abe30e8f-9740-4c97-9b08-1eeac97fd98b
  Args:
    type: :Man
    source: David_Nightingale_Hicks
  AssignClass (0771a615-7023-46c4-bf9a-2aae3fcbfbe9)
 Call ID: 0771a615-7023-46c4-bf9a-2aae3fcbfbe9
  Args:
    source: David_Nightingale_Hicks
    type: :Person
  AddTriple (d6e4970b-3da2-4af8-ba47-2494704ec457)
 Call ID: d6e4970b-3da2-4af8-ba47-2494704ec457
  Args:
    relation: :hasMother
    source: India_Hicks
    target: Lady_Pamela_Mountbatten
  AddTriple (46faa729-abc1-4839-9a16-85499d1180b0)
 Call ID: 46faa729-abc1-4839-9a16-85499d1180b0
  Args:
    target: David_Nightingale_Hicks
    relation: :hasFather
    source: India_Hicks
  AssignClass (35383266-354e-4087-9270-316204847cc7)
 Call ID: 35383266-354e-4087-9270-316204847cc7
  Args:
    source: David_Flint_Wood
    type: :Man
  AssignClass (d52f42d0-3b10-4ec2-85a1-d1731e698e89)
 Call ID: d52f42d0-3b10-4ec2-85a1-d1731e698e89
  Args:
    type: :Person
    source: David_Flint_Wood
  AddTriple (4a9f58f0-6c33-412d-9d35-e98f17c9aaad)
 Call ID: 4a9f58f0-6c33-412d-9d35-e98f17c9aaad
  Args:
    relation: :hasRelation
    source: India_Hicks
    target: David_Flint_Wood
  AssignClass (f0805526-a0fc-4393-bb00-a7f0310b35ac)
 Call ID: f0805526-a0fc-4393-bb00-a7f0310b35ac
  Args:
    type: :Woman
    source: Lady_Helen_Windsor
  AssignClass (59283b3c-674a-4630-be8d-f5641158c811)
 Call ID: 59283b3c-674a-4630-be8d-f5641158c811
  Args:
    type: :Person
    source: Lady_Helen_Windsor
  AddTriple (8a2589f2-2421-40e3-95af-a22e41a30410)
 Call ID: 8a2589f2-2421-40e3-95af-a22e41a30410
  Args:
    relation: :isBloodrelationOf
    source: India_Hicks
    target: Lady_Helen_Windsor
  AssignClass (55dcc0fd-c4ca-410a-beed-c1a4d235b7c6)
 Call ID: 55dcc0fd-c4ca-410a-beed-c1a4d235b7c6
  Args:
    type: :Woman
    source: Susannah_Constantine
  AssignClass (5f40ceef-2e50-4563-97ad-689b8057c7f1)
 Call ID: 5f40ceef-2e50-4563-97ad-689b8057c7f1
  Args:
    source: Susannah_Constantine
    type: :Person
  AssignClass (f9668911-b418-43be-9258-6d463b9ddecc)
 Call ID: f9668911-b418-43be-9258-6d463b9ddecc
  Args:
    source: David_Armstrong-Jones
    type: :Man
  AssignClass (5ba6cd56-9a19-4d59-ad82-2cb059c9498d)
 Call ID: 5ba6cd56-9a19-4d59-ad82-2cb059c9498d
  Args:
    type: :Person
    source: David_Armstrong-Jones
  AddTriple (148a344c-56a7-4651-bd73-276dfb8bee0e)
 Call ID: 148a344c-56a7-4651-bd73-276dfb8bee0e
  Args:
    source: India_Hicks
    relation: :isBloodrelationOf
    target: David_Armstrong-Jones
  AssignClass (e437150f-bd1f-4585-9c30-d4877d52757f)
 Call ID: e437150f-bd1f-4585-9c30-d4877d52757f
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (4127c518-65b7-49e0-a5b7-28f42d24f8e8)
 Call ID: 4127c518-65b7-49e0-a5b7-28f42d24f8e8
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AssignClass (1a220a04-af92-47f5-a1e0-5c054f5cf60e)
 Call ID: 1a220a04-af92-47f5-a1e0-5c054f5cf60e
  Args:
    source: Charles_III
    type: :Man
  AssignClass (d5d02283-a1c3-4f1a-8bd9-db8c7151836f)
 Call ID: d5d02283-a1c3-4f1a-8bd9-db8c7151836f
  Args:
    source: Charles_III
    type: :Person
  AssignClass (4ecd5ce3-0ce5-41a4-926a-48cd0b84cc37)
 Call ID: 4ecd5ce3-0ce5-41a4-926a-48cd0b84cc37
  Args:
    type: :Woman
    source: Lady_Diana_Spencer
  AssignClass (b74faaaf-6abb-4fff-96a1-7952c61ba094)
 Call ID: b74faaaf-6abb-4fff-96a1-7952c61ba094
  Args:
    source: Lady_Diana_Spencer
    type: :Person
  AssignClass (1834931f-fc4c-4fbd-8de4-47ffce90fd1a)
 Call ID: 1834931f-fc4c-4fbd-8de4-47ffce90fd1a
  Args:
    source: Prince_William
    type: :Man
  AssignClass (22bd6659-ed61-439c-9e34-6eb132fe34d5)
 Call ID: 22bd6659-ed61-439c-9e34-6eb132fe34d5
  Args:
    type: :Person
    source: Prince_William
  AssignClass (77d53f0a-c484-42b4-bead-a8a8dc32ef34)
 Call ID: 77d53f0a-c484-42b4-bead-a8a8dc32ef34
  Args:
    source: Catherine_Middleton
    type: :Woman
  AssignClass (d14c1569-995b-43ce-8af5-49e9cc52b5f8)
 Call ID: d14c1569-995b-43ce-8af5-49e9cc52b5f8
  Args:
    type: :Person
    source: Catherine_Middleton
  AssignClass (9a990b7e-08ef-47cf-a188-16de2b3c2caa)
 Call ID: 9a990b7e-08ef-47cf-a188-16de2b3c2caa
  Args:
    type: :Woman
    source: Linda_Griffin
  AssignClass (c2d8bd56-77bd-49ae-89b4-24889ef52a0e)
 Call ID: c2d8bd56-77bd-49ae-89b4-24889ef52a0e
  Args:
    source: Linda_Griffin
    type: :Person
  AssignClass (c3c0d572-cca4-4941-93e6-45a6c76ff853)
 Call ID: c3c0d572-cca4-4941-93e6-45a6c76ff853
  Args:
    source: Nicholas_Keuper
    type: :Man
  AssignClass (96e26863-51df-4a3d-9703-aecedb404735)
 Call ID: 96e26863-51df-4a3d-9703-aecedb404735
  Args:
    source: Nicholas_Keuper
    type: :Person
  AssignClass (3715c000-cc56-46ae-82e4-0e1cc57c0dbc)
 Call ID: 3715c000-cc56-46ae-82e4-0e1cc57c0dbc
  Args:
    source: HauteLook
    type: :DomainEntity
  Finish (e2c7aa84-f3de-4d72-8cfc-03095458a43c)
 Call ID: e2c7aa84-f3de-4d72-8cfc-03095458a43c
  Args: