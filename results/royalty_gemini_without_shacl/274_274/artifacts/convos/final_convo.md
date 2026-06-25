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
  AssignClass (ed33e6ae-7066-42a9-b7d5-70570e0a73d3)
 Call ID: ed33e6ae-7066-42a9-b7d5-70570e0a73d3
  Args:
    source: Lady_Amelia_Windsor
    type: :Woman
  AssignClass (bc580dd3-1590-40d5-9eff-09a6216762ba)
 Call ID: bc580dd3-1590-40d5-9eff-09a6216762ba
  Args:
    type: :Person
    source: Lady_Amelia_Windsor
  AddLiteral (e6bc908f-c8ca-420f-89a1-0d0327a6a904)
 Call ID: e6bc908f-c8ca-420f-89a1-0d0327a6a904
  Args:
    literal_value: 1995
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Lady_Amelia_Windsor
  AssignClass (e4143ea8-d9e1-40f0-9cd9-effe015ab48f)
 Call ID: e4143ea8-d9e1-40f0-9cd9-effe015ab48f
  Args:
    source: George_Windsor_Earl_of_St_Andrews
    type: :Man
  AssignClass (5068ce07-358c-4846-90aa-203a3612b1ad)
 Call ID: 5068ce07-358c-4846-90aa-203a3612b1ad
  Args:
    type: :Person
    source: George_Windsor_Earl_of_St_Andrews
  AssignClass (39188f34-63f6-47c9-8041-c1c9a44cfe41)
 Call ID: 39188f34-63f6-47c9-8041-c1c9a44cfe41
  Args:
    type: :Woman
    source: Sylvana_Tomaselli
  AssignClass (affe91fc-5485-45aa-a9ac-7b2147ea4f11)
 Call ID: affe91fc-5485-45aa-a9ac-7b2147ea4f11
  Args:
    source: Sylvana_Tomaselli
    type: :Person
  AddTriple (f4cae489-6dc9-48da-aa26-9fe0a9a54815)
 Call ID: f4cae489-6dc9-48da-aa26-9fe0a9a54815
  Args:
    target: George_Windsor_Earl_of_St_Andrews
    source: Lady_Amelia_Windsor
    relation: :hasFather
  AddTriple (8cb7d7c9-9ef9-4606-a7f9-a7ab2e472281)
 Call ID: 8cb7d7c9-9ef9-4606-a7f9-a7ab2e472281
  Args:
    source: Lady_Amelia_Windsor
    target: Sylvana_Tomaselli
    relation: :hasMother
  AssignClass (061a7618-ed39-488c-8f4f-ae8e8c49cd85)
 Call ID: 061a7618-ed39-488c-8f4f-ae8e8c49cd85
  Args:
    source: Prince_Edward_Duke_of_Kent
    type: :Man
  AssignClass (6b9b4642-1ba7-4cc4-a173-8eaf22a3d843)
 Call ID: 6b9b4642-1ba7-4cc4-a173-8eaf22a3d843
  Args:
    type: :Person
    source: Prince_Edward_Duke_of_Kent
  AssignClass (4c1b1de2-fb0c-4664-a8dd-6a4c1985b150)
 Call ID: 4c1b1de2-fb0c-4664-a8dd-6a4c1985b150
  Args:
    type: :Woman
    source: Katharine_Duchess_of_Kent
  AssignClass (312adec5-3806-43b0-b1c1-8d64d094cdca)
 Call ID: 312adec5-3806-43b0-b1c1-8d64d094cdca
  Args:
    source: Katharine_Duchess_of_Kent
    type: :Person
  AddTriple (e6b95940-a42d-41e7-b78a-f552e378c374)
 Call ID: e6b95940-a42d-41e7-b78a-f552e378c374
  Args:
    relation: :hasFather
    source: George_Windsor_Earl_of_St_Andrews
    target: Prince_Edward_Duke_of_Kent
  AddTriple (8004204a-9d9b-4d9d-a802-2b2a3613d39f)
 Call ID: 8004204a-9d9b-4d9d-a802-2b2a3613d39f
  Args:
    target: Katharine_Duchess_of_Kent
    source: George_Windsor_Earl_of_St_Andrews
    relation: :hasMother
  AssignClass (3dbb3cae-c3be-4d59-865e-704a0137deab)
 Call ID: 3dbb3cae-c3be-4d59-865e-704a0137deab
  Args:
    source: Edward_Windsor_Lord_Downpatrick
    type: :Man
  AssignClass (90aa590f-4fb6-40d2-bf47-9706b9c1e0ab)
 Call ID: 90aa590f-4fb6-40d2-bf47-9706b9c1e0ab
  Args:
    source: Edward_Windsor_Lord_Downpatrick
    type: :Person
  AssignClass (b2aa90ed-87b9-4948-8f00-0b7868d61fd2)
 Call ID: b2aa90ed-87b9-4948-8f00-0b7868d61fd2
  Args:
    type: :Woman
    source: Lady_Marina_Windsor
  AssignClass (5aae9925-c790-440d-a09c-b914e45aa40b)
 Call ID: 5aae9925-c790-440d-a09c-b914e45aa40b
  Args:
    source: Lady_Marina_Windsor
    type: :Person
  AddTriple (59071ba9-bb40-4748-af07-20b3f7d8160d)
 Call ID: 59071ba9-bb40-4748-af07-20b3f7d8160d
  Args:
    relation: :isSiblingOf
    source: Lady_Amelia_Windsor
    target: Edward_Windsor_Lord_Downpatrick
  AddTriple (c234ee8d-46e0-4df0-80fb-db0ae80bb31b)
 Call ID: c234ee8d-46e0-4df0-80fb-db0ae80bb31b
  Args:
    target: Lady_Marina_Windsor
    source: Lady_Amelia_Windsor
    relation: :isSiblingOf
  AssignClass (e617eb3a-748b-4fa3-9855-ed8279c07e25)
 Call ID: e617eb3a-748b-4fa3-9855-ed8279c07e25
  Args:
    source: Prince_George_Duke_of_Kent
    type: :Man
  AssignClass (dd9dcecd-180e-4aa1-a0d4-4bb7b18e2209)
 Call ID: dd9dcecd-180e-4aa1-a0d4-4bb7b18e2209
  Args:
    source: Prince_George_Duke_of_Kent
    type: :Person
  AssignClass (2fe1f4bc-575e-4bca-a7cf-a0ac5e99f19c)
 Call ID: 2fe1f4bc-575e-4bca-a7cf-a0ac5e99f19c
  Args:
    type: :Woman
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (4d9eea51-2f7a-4fdf-a3f7-e6377da185c4)
 Call ID: 4d9eea51-2f7a-4fdf-a3f7-e6377da185c4
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    type: :Person
  AddTriple (4f928952-0396-4c47-b395-a7c445601094)
 Call ID: 4f928952-0396-4c47-b395-a7c445601094
  Args:
    target: Prince_George_Duke_of_Kent
    source: Prince_Edward_Duke_of_Kent
    relation: :hasFather
  AddTriple (ca6f82e6-90f5-4c4a-8b75-03ae1c2b63a8)
 Call ID: ca6f82e6-90f5-4c4a-8b75-03ae1c2b63a8
  Args:
    relation: :hasMother
    source: Prince_Edward_Duke_of_Kent
    target: Princess_Marina_of_Greece_and_Denmark
  AssignClass (594edd4a-3061-40d2-b4c1-8928f5a47950)
 Call ID: 594edd4a-3061-40d2-b4c1-8928f5a47950
  Args:
    source: George_V
    type: :Man
  AssignClass (171fe149-d01f-44e1-8570-42a5b6978f4e)
 Call ID: 171fe149-d01f-44e1-8570-42a5b6978f4e
  Args:
    source: George_V
    type: :Person
  AssignClass (7d32ec15-6f95-4295-b985-64bb48be97b7)
 Call ID: 7d32ec15-6f95-4295-b985-64bb48be97b7
  Args:
    type: :Woman
    source: Mary_of_Teck
  AssignClass (aa6ee6a3-f279-404d-a9e0-3106aefc603e)
 Call ID: aa6ee6a3-f279-404d-a9e0-3106aefc603e
  Args:
    source: Mary_of_Teck
    type: :Person
  AddTriple (f08528d7-42c1-4936-9e84-b2ae92864e54)
 Call ID: f08528d7-42c1-4936-9e84-b2ae92864e54
  Args:
    source: Prince_George_Duke_of_Kent
    target: George_V
    relation: :hasFather
  AddTriple (ebd1826c-d63a-45e4-8e4a-67b3dc75016c)
 Call ID: ebd1826c-d63a-45e4-8e4a-67b3dc75016c
  Args:
    source: Prince_George_Duke_of_Kent
    target: Mary_of_Teck
    relation: :hasMother
  AssignClass (d0593cee-0a97-4993-b730-e508f936672c)
 Call ID: d0593cee-0a97-4993-b730-e508f936672c
  Args:
    source: Sir_William_Worsley_4th_Baronet
    type: :Man
  AssignClass (88b36cb7-fef3-449e-a7ae-02f039fe10ac)
 Call ID: 88b36cb7-fef3-449e-a7ae-02f039fe10ac
  Args:
    type: :Person
    source: Sir_William_Worsley_4th_Baronet
  AddTriple (75783aee-faf3-42dd-b590-a8878246b7f5)
 Call ID: 75783aee-faf3-42dd-b590-a8878246b7f5
  Args:
    relation: :hasFather
    target: Sir_William_Worsley_4th_Baronet
    source: Katharine_Duchess_of_Kent
  AssignClass (654ecd7c-268f-447e-b1bb-9aa7999fb5d9)
 Call ID: 654ecd7c-268f-447e-b1bb-9aa7999fb5d9
  Args:
    source: Lord_Nicholas_Windsor
    type: :Man
  AssignClass (9a078c2c-317c-4958-91f6-4dc73c8edeba)
 Call ID: 9a078c2c-317c-4958-91f6-4dc73c8edeba
  Args:
    source: Lord_Nicholas_Windsor
    type: :Person
  AddTriple (a7019f63-dcea-42da-9620-000faf9416bf)
 Call ID: a7019f63-dcea-42da-9620-000faf9416bf
  Args:
    relation: :hasFather
    source: Lord_Nicholas_Windsor
    target: Prince_Edward_Duke_of_Kent
  AddTriple (67090ebb-0e48-43f1-b0ed-68652bada43b)
 Call ID: 67090ebb-0e48-43f1-b0ed-68652bada43b
  Args:
    target: Katharine_Duchess_of_Kent
    source: Lord_Nicholas_Windsor
    relation: :hasMother
  Finish (b5075ef5-4c56-492f-bffb-638ae3baffc6)
 Call ID: b5075ef5-4c56-492f-bffb-638ae3baffc6
  Args: