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
Lady Amelia Sophia Theodora Mary Margaret Windsor (born 24 August 1995) is a British fashion model and a member of the extended British royal family.
She is a granddaughter of Prince Edward, Duke of Kent, and therefore a great-great-granddaughter of George V and Queen Mary.
Early life and family

Lady Amelia Sophia Theodora Mary Margaret Windsor was born on 24 August 1995 at the Rosie Hospital in Cambridge.
She is the youngest child of George Windsor, Earl of St Andrews, and his wife, Sylvana Tomaselli.
Her paternal grandfather, Prince Edward, Duke of Kent, is a first cousin of Elizabeth II and her father is a second cousin of Charles III.
Her paternal great grandparents were Prince George, Duke of Kent, and Princess Marina of Greece and Denmark, a granddaughter of George I of Greece and first cousin of Prince Philip, Duke of Edinburgh.
Her paternal great-great grandparents were George V and Mary of Teck.
Her paternal grandmother, Katharine, Duchess of Kent, was the daughter of Sir William Worsley, 4th Baronet.
Amelia descends maternally from the Austrian Tomaselli family.
She is the younger sister of Edward Windsor, Lord Downpatrick, and Lady Marina Windsor.
She is a third cousin of William, Prince of Wales, and Prince Harry, Duke of Sussex.
Career

Amelia is signed with Storm Model Management.
In 2018, Amelia released a collaboration with Penelope Chilvers for a line of shoes, and modelled for the line in a video campaign in Spain.
Amelia has worked for Chanel, Azzedine Alaia, and interned at BVLGARI.
In October 2018 Amelia became the spokesmodel for British make-up brand Illamasqua.
In 2020, Amelia began contributing to a new environmental platform called Talia Collective, writing about eco-travel and lifestyle.
Succession rights

Amelia's father, the Earl of St Andrews, lost his succession rights to the British throne according to the Act of Settlement 1701 as a consequence of marrying a Catholic.
Although her grandmother, the Duchess of Kent, had converted to Catholicism in 1994, it did not remove her grandfather, Prince Edward, from the line of succession as the duchess was Anglican at the time of their wedding in 1961 and the Act of Settlement 1701 did not take into consideration a person married to someone in the line of succession converting to Catholicism.
Her uncle, Lord Nicholas Windsor, converted to Catholicism in 2001, which removed him from the line of succession.
In 2013, the Succession to the Crown Act was passed, giving Amelia's father succession rights once again.
Amelia's two older siblings were confirmed in the Catholic faith and therefore lost their succession rights.
Personal life

After graduating from St Mary's School, Ascot, Amelia spent a gap year in India and Thailand before studying French and Italian at the University of Edinburgh.
Amelia was named in the Vanity Fair International Best Dressed List in 2017.
Amelia lives in a flat in Notting Hill, West London.



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
  AssignClass (035b1bee-fe42-4c5c-a8cd-21f0eb73944d)
 Call ID: 035b1bee-fe42-4c5c-a8cd-21f0eb73944d
  Args:
    type: :Woman
    source: Amelia_Windsor
  AssignClass (5669cd28-9462-44ab-b49c-25f0317ca9c4)
 Call ID: 5669cd28-9462-44ab-b49c-25f0317ca9c4
  Args:
    type: :Person
    source: Amelia_Windsor
  AddLiteral (ee836808-b5c9-47b7-ae15-a08ac63e7e06)
 Call ID: ee836808-b5c9-47b7-ae15-a08ac63e7e06
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Amelia_Windsor
    literal_value: 1995
  AssignClass (a23618b4-5ba9-497d-a894-4c0ac3bb77f9)
 Call ID: a23618b4-5ba9-497d-a894-4c0ac3bb77f9
  Args:
    type: :Man
    source: George_Windsor_Earl_of_St_Andrews
  AssignClass (9cbd08dd-8bc0-406b-8367-079c6cc25d88)
 Call ID: 9cbd08dd-8bc0-406b-8367-079c6cc25d88
  Args:
    type: :Person
    source: George_Windsor_Earl_of_St_Andrews
  AssignClass (341886e0-bee3-4a11-bd47-c045a6012a05)
 Call ID: 341886e0-bee3-4a11-bd47-c045a6012a05
  Args:
    type: :Woman
    source: Sylvana_Tomaselli
  AssignClass (f3d1a856-a6c7-4105-bbfd-77597bc81c6e)
 Call ID: f3d1a856-a6c7-4105-bbfd-77597bc81c6e
  Args:
    type: :Person
    source: Sylvana_Tomaselli
  AddTriple (c438b1c4-3bb1-45ea-a303-cb2031110eb7)
 Call ID: c438b1c4-3bb1-45ea-a303-cb2031110eb7
  Args:
    source: Amelia_Windsor
    relation: :hasFather
    target: George_Windsor_Earl_of_St_Andrews
  AddTriple (0811a706-a795-4e3d-a2ca-24cd710bb63b)
 Call ID: 0811a706-a795-4e3d-a2ca-24cd710bb63b
  Args:
    source: Amelia_Windsor
    target: Sylvana_Tomaselli
    relation: :hasMother
  AssignClass (3b8d5625-5eb2-4486-93fa-2f11408db9ed)
 Call ID: 3b8d5625-5eb2-4486-93fa-2f11408db9ed
  Args:
    type: :Man
    source: Prince_Edward_Duke_of_Kent
  AssignClass (0ff27057-ca96-4a9c-b3b3-e30872c391d1)
 Call ID: 0ff27057-ca96-4a9c-b3b3-e30872c391d1
  Args:
    type: :Person
    source: Prince_Edward_Duke_of_Kent
  AssignClass (0c95f283-17cd-4a01-bcda-791360ea4351)
 Call ID: 0c95f283-17cd-4a01-bcda-791360ea4351
  Args:
    type: :Woman
    source: Katharine_Duchess_of_Kent
  AssignClass (f32f0324-e624-4e87-ae66-b78ef325be73)
 Call ID: f32f0324-e624-4e87-ae66-b78ef325be73
  Args:
    type: :Person
    source: Katharine_Duchess_of_Kent
  AddTriple (4b7cfe65-816d-4f28-8a38-4f4c5340d610)
 Call ID: 4b7cfe65-816d-4f28-8a38-4f4c5340d610
  Args:
    source: George_Windsor_Earl_of_St_Andrews
    relation: :hasFather
    target: Prince_Edward_Duke_of_Kent
  AddTriple (24832229-48b0-4f33-8299-d4f92a70ff0c)
 Call ID: 24832229-48b0-4f33-8299-d4f92a70ff0c
  Args:
    source: George_Windsor_Earl_of_St_Andrews
    relation: :hasMother
    target: Katharine_Duchess_of_Kent
  AssignClass (c8ce83a1-545a-4676-870f-4f781ca41b77)
 Call ID: c8ce83a1-545a-4676-870f-4f781ca41b77
  Args:
    type: :Man
    source: Edward_Windsor_Lord_Downpatrick
  AssignClass (51078106-8d5f-49b3-9565-fe7cff9ed2e2)
 Call ID: 51078106-8d5f-49b3-9565-fe7cff9ed2e2
  Args:
    type: :Person
    source: Edward_Windsor_Lord_Downpatrick
  AssignClass (35bae4c1-1214-4e9f-843f-b256b4c98cfa)
 Call ID: 35bae4c1-1214-4e9f-843f-b256b4c98cfa
  Args:
    type: :Woman
    source: Lady_Marina_Windsor
  AssignClass (ba113111-a907-4207-85d9-8de8fe110dac)
 Call ID: ba113111-a907-4207-85d9-8de8fe110dac
  Args:
    type: :Person
    source: Lady_Marina_Windsor
  AddTriple (d1e0410c-f694-482e-87b3-070e619a80b3)
 Call ID: d1e0410c-f694-482e-87b3-070e619a80b3
  Args:
    target: Edward_Windsor_Lord_Downpatrick
    relation: :hasBrother
    source: Amelia_Windsor
  AddTriple (b7664ff6-b241-4992-a139-d9f3cd0fe6c3)
 Call ID: b7664ff6-b241-4992-a139-d9f3cd0fe6c3
  Args:
    relation: :hasSister
    target: Lady_Marina_Windsor
    source: Amelia_Windsor
  AssignClass (0577dc33-5125-4272-afa7-0d64f060d2e5)
 Call ID: 0577dc33-5125-4272-afa7-0d64f060d2e5
  Args:
    type: :Man
    source: Lord_Nicholas_Windsor
  AssignClass (344c1acc-f343-4426-b435-70effc8d630c)
 Call ID: 344c1acc-f343-4426-b435-70effc8d630c
  Args:
    type: :Person
    source: Lord_Nicholas_Windsor
  AddTriple (8839d9af-9842-4577-bbd3-be14b1b09534)
 Call ID: 8839d9af-9842-4577-bbd3-be14b1b09534
  Args:
    source: Lord_Nicholas_Windsor
    relation: :hasFather
    target: Prince_Edward_Duke_of_Kent
  AddTriple (30ce8113-000b-47af-b492-fd0243225768)
 Call ID: 30ce8113-000b-47af-b492-fd0243225768
  Args:
    source: Lord_Nicholas_Windsor
    target: Katharine_Duchess_of_Kent
    relation: :hasMother
  AssignClass (957c602c-1bae-4a28-96f5-acde6a35d205)
 Call ID: 957c602c-1bae-4a28-96f5-acde6a35d205
  Args:
    type: :Man
    source: Prince_George_Duke_of_Kent
  AssignClass (5c532cc5-153c-4c15-af9f-4aa0a5bb4059)
 Call ID: 5c532cc5-153c-4c15-af9f-4aa0a5bb4059
  Args:
    type: :Person
    source: Prince_George_Duke_of_Kent
  AssignClass (81036a4e-3b5f-4fa1-bb2d-9f3bd2bbe77e)
 Call ID: 81036a4e-3b5f-4fa1-bb2d-9f3bd2bbe77e
  Args:
    type: :Woman
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (5da543a9-3147-41b3-a1b6-47c697f35027)
 Call ID: 5da543a9-3147-41b3-a1b6-47c697f35027
  Args:
    type: :Person
    source: Princess_Marina_of_Greece_and_Denmark
  AddTriple (c3c98c47-b94a-4c6a-a8e0-d4c00e43e38b)
 Call ID: c3c98c47-b94a-4c6a-a8e0-d4c00e43e38b
  Args:
    source: Prince_Edward_Duke_of_Kent
    relation: :hasFather
    target: Prince_George_Duke_of_Kent
  AddTriple (a0a476f6-025e-4bb8-9a76-350e1d0cde4a)
 Call ID: a0a476f6-025e-4bb8-9a76-350e1d0cde4a
  Args:
    source: Prince_Edward_Duke_of_Kent
    target: Princess_Marina_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (f8b4280a-5552-4518-9328-a8c880d2d086)
 Call ID: f8b4280a-5552-4518-9328-a8c880d2d086
  Args:
    type: :Man
    source: George_V
  AssignClass (08ca15d5-ef30-491a-a6fa-005ad959f8f8)
 Call ID: 08ca15d5-ef30-491a-a6fa-005ad959f8f8
  Args:
    type: :Person
    source: George_V
  AssignClass (a964c86c-0e53-4085-bdea-074f936a60ae)
 Call ID: a964c86c-0e53-4085-bdea-074f936a60ae
  Args:
    type: :Woman
    source: Mary_of_Teck
  AssignClass (64d5c65f-0e4c-4301-8477-901533c32484)
 Call ID: 64d5c65f-0e4c-4301-8477-901533c32484
  Args:
    type: :Person
    source: Mary_of_Teck
  AddTriple (e06e718b-b6f9-4016-a705-7032b8c5b63a)
 Call ID: e06e718b-b6f9-4016-a705-7032b8c5b63a
  Args:
    target: George_V
    relation: :hasFather
    source: Prince_George_Duke_of_Kent
  AddTriple (a35f1609-3d4b-41ed-8240-dc1f2ba06708)
 Call ID: a35f1609-3d4b-41ed-8240-dc1f2ba06708
  Args:
    target: Mary_of_Teck
    relation: :hasMother
    source: Prince_George_Duke_of_Kent
  AssignClass (063ac8bb-f367-478d-806e-246fc4def963)
 Call ID: 063ac8bb-f367-478d-806e-246fc4def963
  Args:
    type: :Man
    source: Sir_William_Worsley_4th_Baronet
  AssignClass (81e4b181-60ab-484d-9be8-8fdeb1b527d2)
 Call ID: 81e4b181-60ab-484d-9be8-8fdeb1b527d2
  Args:
    type: :Person
    source: Sir_William_Worsley_4th_Baronet
  AddTriple (df18b81a-6d19-4297-9e17-b46fa29757a2)
 Call ID: df18b81a-6d19-4297-9e17-b46fa29757a2
  Args:
    source: Katharine_Duchess_of_Kent
    target: Sir_William_Worsley_4th_Baronet
    relation: :hasFather
  Finish (318792ae-593e-4e66-894e-205afba0583a)
 Call ID: 318792ae-593e-4e66-894e-205afba0583a
  Args: