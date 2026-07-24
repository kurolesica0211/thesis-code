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
Lady Margarita Elizabeth Rose Alleyne Armstrong-Jones (born 14 May 2002) is a member of the British royal family.
She is the granddaughter of Princess Margaret and the grandniece of Queen Elizabeth II.
Lady Margarita is a jewellery designer and the creator of the bespoke jewellery label Matita.
Early life and family

Lady Margarita was born The Honourable Margarita Armstrong-Jones on 14 May 2002 at Portland Hospital in London.
She is the daughter of David Armstrong-Jones, 2nd Earl of Snowdon, who was styled as Viscount Linley at the time of her birth, and The Honourable Serena Stanhope.
On her father's side, she is the granddaughter of Princess Margaret, Countess of Snowdon and Antony Armstrong-Jones, 1st Earl of Snowdon and a great-granddaughter of King George VI.
On her mother's side, she is the granddaughter of Charles Stanhope, 12th Earl of Harrington and a descendant of Charles II.
She was baptised Margarita Elizabeth Rose Alleyne, and was named after her grandmother and great-grandmother, Queen Elizabeth The Queen Mother.
Her father succeeded his father as the Earl of Snowdon in 2017, which entitled her to use the title Lady.
Lady Margarita's parents separated in 2020.
Education

Lady Margarita was first educated at Garden House School, a private school in the Royal Borough of Kensington and Chelsea before attending St Mary's School Ascot, a Catholic all-girls boarding school.
Lady Margarita took life drawing, pottery, and watercolour painting courses at a small art school in Oxford.
In September 2022, Lady Margarita enrolled as a student at La Haute École de Joaillerie in Paris to study jewellery design, stonesetting, and wax carving.
Public role and royal appearances

In 2008, she attended the wedding of Peter Phillips, son of the Princess Royal, to Autumn Kelly at St George's Chapel, Windsor and appeared with the royal family for photographs the following day.
That same year, she accompanied her aunt, Lady Sarah Chatto, to the 60th birthday brunch for Charles, Prince of Wales at the Goring Hotel.
In 2011, Lady Margarita served as a bridesmaid at the wedding of Prince William and Catherine Middleton alongside Lady Louise Windsor, Eliza Lopes, and Grace van Cutsem.
Her elder brother, Viscount Linley, served as a page of honour to Elizabeth II.
On 30 March 2012, she attended a Service of Thanksgiving for the Queen Mother and Princess Margaret at St George's Chapel.
In 2018, Lady Margarita attended the wedding of Prince Harry and Meghan Markle and the wedding of Princess Eugenie and Jack Brooksbank.
Along with other members of the extended royal family, she attended the funeral of Prince Philip, Duke of Edinburgh in 2021 and the state funeral of Elizabeth II in 2022.
Lady Margarita was present at the Coronation of Charles III and Camilla on 6 May 2023.
Lady Margarita also attends the annual Trooping of the Colour, having accompanied Elizabeth II in the past.
She attends Christmas services with the royal family at St Mary Magdalene Church, Sandringham, and attended the annual Queen's Christmas Lunch at Buckingham Palace.
Career

Lady Margarita made her modelling debut in 2011 for Kids Company.
Personal life

In September 2022, Lady Margarita moved to Paris, renting a flat near the Bastille where she lives with her two best friends.



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
  AssignClass (da2c60d8-0900-4b77-8ea4-499278e819fe)
 Call ID: da2c60d8-0900-4b77-8ea4-499278e819fe
  Args:
    type: :Person
    source: Lady_Margarita_Armstrong-Jones
  AssignClass (9c3c97e7-12f0-4a21-b57e-0f398fa46e7a)
 Call ID: 9c3c97e7-12f0-4a21-b57e-0f398fa46e7a
  Args:
    type: :Woman
    source: Lady_Margarita_Armstrong-Jones
  AddLiteral (03464634-3991-4e30-9919-5c1783fe0605)
 Call ID: 03464634-3991-4e30-9919-5c1783fe0605
  Args:
    source: Lady_Margarita_Armstrong-Jones
    relation: :hasBirthYear
    literal_value: 2002
    literal_type: xsd:positiveInteger
  AssignClass (2b34bab5-1087-40f5-ab4f-0f0e38c511dd)
 Call ID: 2b34bab5-1087-40f5-ab4f-0f0e38c511dd
  Args:
    type: :Person
    source: David_Armstrong-Jones
  AssignClass (549b45ca-3440-4e6f-8306-39cf5036eedc)
 Call ID: 549b45ca-3440-4e6f-8306-39cf5036eedc
  Args:
    type: :Man
    source: David_Armstrong-Jones
  AssignClass (c94ef636-f28c-4fe6-99ab-ad0ec47eee04)
 Call ID: c94ef636-f28c-4fe6-99ab-ad0ec47eee04
  Args:
    type: :Person
    source: Serena_Stanhope
  AssignClass (216d4660-3efe-4733-b344-92509962e182)
 Call ID: 216d4660-3efe-4733-b344-92509962e182
  Args:
    type: :Woman
    source: Serena_Stanhope
  AddTriple (f2312919-86f5-41e2-902a-ffdeab0dc748)
 Call ID: f2312919-86f5-41e2-902a-ffdeab0dc748
  Args:
    relation: :hasFather
    source: Lady_Margarita_Armstrong-Jones
    target: David_Armstrong-Jones
  AddTriple (ab33ab21-8db0-4b53-8c1e-4e580e516eed)
 Call ID: ab33ab21-8db0-4b53-8c1e-4e580e516eed
  Args:
    target: Serena_Stanhope
    source: Lady_Margarita_Armstrong-Jones
    relation: :hasMother
  AssignClass (ce52fe19-1dba-4b03-bffe-eedf9c154403)
 Call ID: ce52fe19-1dba-4b03-bffe-eedf9c154403
  Args:
    type: :Person
    source: Princess_Margaret
  AssignClass (30c31375-28cb-4e64-97d5-e8d1898e3253)
 Call ID: 30c31375-28cb-4e64-97d5-e8d1898e3253
  Args:
    type: :Woman
    source: Princess_Margaret
  AssignClass (39df3848-b785-4c37-b57c-9f169c3d11d4)
 Call ID: 39df3848-b785-4c37-b57c-9f169c3d11d4
  Args:
    type: :Person
    source: Antony_Armstrong-Jones
  AssignClass (ff9a7502-b813-48ba-951a-055eff977f61)
 Call ID: ff9a7502-b813-48ba-951a-055eff977f61
  Args:
    type: :Man
    source: Antony_Armstrong-Jones
  AddTriple (cd1d03e5-b0c6-4c35-8acf-8888d305c38d)
 Call ID: cd1d03e5-b0c6-4c35-8acf-8888d305c38d
  Args:
    target: Princess_Margaret
    source: David_Armstrong-Jones
    relation: :hasMother
  AddTriple (4205ff70-0d4e-4aef-81b5-960333a53752)
 Call ID: 4205ff70-0d4e-4aef-81b5-960333a53752
  Args:
    relation: :hasFather
    source: David_Armstrong-Jones
    target: Antony_Armstrong-Jones
  AssignClass (fef57249-76a0-40ea-9626-342586a1e6c2)
 Call ID: fef57249-76a0-40ea-9626-342586a1e6c2
  Args:
    type: :Person
    source: Charles_Stanhope
  AssignClass (481cfacb-faed-4adb-bca9-047e035e50fa)
 Call ID: 481cfacb-faed-4adb-bca9-047e035e50fa
  Args:
    type: :Man
    source: Charles_Stanhope
  AddTriple (b2ac5d2e-6154-4777-9608-4942bb815ead)
 Call ID: b2ac5d2e-6154-4777-9608-4942bb815ead
  Args:
    target: Charles_Stanhope
    source: Serena_Stanhope
    relation: :hasFather
  AssignClass (7d5084d5-2ecf-4120-9431-111c943d8126)
 Call ID: 7d5084d5-2ecf-4120-9431-111c943d8126
  Args:
    type: :Person
    source: Lady_Sarah_Chatto
  AssignClass (4c90e8b9-74c7-4080-b690-631ce712e6e6)
 Call ID: 4c90e8b9-74c7-4080-b690-631ce712e6e6
  Args:
    type: :Woman
    source: Lady_Sarah_Chatto
  AddTriple (8309df18-1f69-46b8-bcc0-4d584b9582b7)
 Call ID: 8309df18-1f69-46b8-bcc0-4d584b9582b7
  Args:
    target: Lady_Sarah_Chatto
    source: Lady_Margarita_Armstrong-Jones
    relation: :hasRelation
  AssignClass (90901683-5968-4c7f-981a-8fe9432b40c6)
 Call ID: 90901683-5968-4c7f-981a-8fe9432b40c6
  Args:
    type: :Person
    source: Viscount_Linley
  AssignClass (7a1c5a4d-c041-4f76-acef-aa1a94911d68)
 Call ID: 7a1c5a4d-c041-4f76-acef-aa1a94911d68
  Args:
    type: :Man
    source: Viscount_Linley
  AddTriple (2bb3a138-8254-415c-9d86-d2b3c101887e)
 Call ID: 2bb3a138-8254-415c-9d86-d2b3c101887e
  Args:
    relation: :hasBrother
    source: Lady_Margarita_Armstrong-Jones
    target: Viscount_Linley
  Finish (f29be082-c979-4c9a-957c-ea8c72a5eb4e)
 Call ID: f29be082-c979-4c9a-957c-ea8c72a5eb4e
  Args: