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
  AssignClass (f331b0d7-7585-4b94-945b-ee54c7b353af)
 Call ID: f331b0d7-7585-4b94-945b-ee54c7b353af
  Args:
    source: Lady_Amelia_Windsor
    type: :Woman
  AssignClass (87b5ce74-3c33-48a4-8ab3-c6cc5f910287)
 Call ID: 87b5ce74-3c33-48a4-8ab3-c6cc5f910287
  Args:
    source: Lady_Amelia_Windsor
    type: :Person
  AddLiteral (8317f0af-6387-433a-99c0-be7f100e17f6)
 Call ID: 8317f0af-6387-433a-99c0-be7f100e17f6
  Args:
    source: Lady_Amelia_Windsor
    literal_type: xsd:integer
    literal_value: 1995
    relation: :hasBirthYear
  AssignClass (ba4ec545-bfe0-46f4-b663-41219e6025b1)
 Call ID: ba4ec545-bfe0-46f4-b663-41219e6025b1
  Args:
    type: :Man
    source: Prince_Edward_Duke_of_Kent
  AssignClass (50e856b8-556b-43c5-aebb-43624077d0e4)
 Call ID: 50e856b8-556b-43c5-aebb-43624077d0e4
  Args:
    source: Prince_Edward_Duke_of_Kent
    type: :Person
  AssignClass (2f276f33-990f-4ae2-ad7a-e7ae4ab23ca7)
 Call ID: 2f276f33-990f-4ae2-ad7a-e7ae4ab23ca7
  Args:
    type: :Man
    source: George_V
  AssignClass (9e0ace80-e5a6-4e15-a31e-9b282415a046)
 Call ID: 9e0ace80-e5a6-4e15-a31e-9b282415a046
  Args:
    type: :Person
    source: George_V
  AssignClass (0d428997-a17e-4456-87e0-212603be7110)
 Call ID: 0d428997-a17e-4456-87e0-212603be7110
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (a1b513d4-1f83-4f1d-8940-4c49d83e5348)
 Call ID: a1b513d4-1f83-4f1d-8940-4c49d83e5348
  Args:
    source: Queen_Mary
    type: :Person
  AddTriple (2f0ee8c1-02f8-475a-a4ba-c83a3d85ca91)
 Call ID: 2f0ee8c1-02f8-475a-a4ba-c83a3d85ca91
  Args:
    relation: :isChildOf
    source: Lady_Amelia_Windsor
    target: Prince_Edward_Duke_of_Kent
  AssignClass (4e65dfe1-011c-43d0-b660-aaec254fa842)
 Call ID: 4e65dfe1-011c-43d0-b660-aaec254fa842
  Args:
    source: George_Windsor_Earl_of_St_Andrews
    type: :Man
  AssignClass (0679875d-879f-4f22-9c83-8d188b64cc5a)
 Call ID: 0679875d-879f-4f22-9c83-8d188b64cc5a
  Args:
    source: George_Windsor_Earl_of_St_Andrews
    type: :Person
  AssignClass (b7d5313c-08ff-449e-9c40-8dca6bcc44de)
 Call ID: b7d5313c-08ff-449e-9c40-8dca6bcc44de
  Args:
    source: Sylvana_Tomaselli
    type: :Woman
  AssignClass (d895df54-8efc-4cbe-bc42-fd2403e282bb)
 Call ID: d895df54-8efc-4cbe-bc42-fd2403e282bb
  Args:
    source: Sylvana_Tomaselli
    type: :Person
  AddTriple (5b5971bb-2264-432d-b735-c90db60ca5b7)
 Call ID: 5b5971bb-2264-432d-b735-c90db60ca5b7
  Args:
    relation: :hasFather
    source: Lady_Amelia_Windsor
    target: George_Windsor_Earl_of_St_Andrews
  AddTriple (892a7690-7bd0-423c-88ca-bdca3c0b68ce)
 Call ID: 892a7690-7bd0-423c-88ca-bdca3c0b68ce
  Args:
    source: Lady_Amelia_Windsor
    target: Sylvana_Tomaselli
    relation: :hasMother
  AssignClass (e83d8952-be15-46bd-bce8-9e1b7a2e027e)
 Call ID: e83d8952-be15-46bd-bce8-9e1b7a2e027e
  Args:
    type: :Man
    source: Edward_Windsor_Lord_Downpatrick
  AssignClass (36a369fb-3996-4990-a883-a3faf4247216)
 Call ID: 36a369fb-3996-4990-a883-a3faf4247216
  Args:
    source: Edward_Windsor_Lord_Downpatrick
    type: :Person
  AssignClass (aa03ad0f-0813-4dfb-bbb0-5278f85e3567)
 Call ID: aa03ad0f-0813-4dfb-bbb0-5278f85e3567
  Args:
    type: :Woman
    source: Lady_Marina_Windsor
  AssignClass (10c8dc9b-92c8-4bf1-840a-4403e96f2396)
 Call ID: 10c8dc9b-92c8-4bf1-840a-4403e96f2396
  Args:
    source: Lady_Marina_Windsor
    type: :Person
  AddTriple (d503aa9b-310f-4dca-8f11-1a9a1d5e4c73)
 Call ID: d503aa9b-310f-4dca-8f11-1a9a1d5e4c73
  Args:
    target: Edward_Windsor_Lord_Downpatrick
    source: Lady_Amelia_Windsor
    relation: :isSiblingOf
  AddTriple (07e68549-878c-41d8-a702-ef190486bf2f)
 Call ID: 07e68549-878c-41d8-a702-ef190486bf2f
  Args:
    target: Lady_Marina_Windsor
    source: Lady_Amelia_Windsor
    relation: :isSiblingOf
  AssignClass (a70fc23c-8e0c-42e7-8668-fd2fd6d2117a)
 Call ID: a70fc23c-8e0c-42e7-8668-fd2fd6d2117a
  Args:
    type: :Man
    source: Prince_George_Duke_of_Kent
  AssignClass (9946f496-1a4e-4203-a6ae-68ff48f0fb8e)
 Call ID: 9946f496-1a4e-4203-a6ae-68ff48f0fb8e
  Args:
    type: :Woman
    source: Princess_Marina_of_Greece_and_Denmark
  AddTriple (43de17bc-2df1-4afc-9aa9-9fb8b5c7d50e)
 Call ID: 43de17bc-2df1-4afc-9aa9-9fb8b5c7d50e
  Args:
    source: Prince_Edward_Duke_of_Kent
    target: Prince_George_Duke_of_Kent
    relation: :hasFather
  AddTriple (572ed570-9dc0-4791-b844-0ec69dd0d53f)
 Call ID: 572ed570-9dc0-4791-b844-0ec69dd0d53f
  Args:
    target: Princess_Marina_of_Greece_and_Denmark
    source: Prince_Edward_Duke_of_Kent
    relation: :hasMother
  AssignClass (2247de78-dc91-4ec8-8121-76c270fc726d)
 Call ID: 2247de78-dc91-4ec8-8121-76c270fc726d
  Args:
    type: :Woman
    source: Katharine_Duchess_of_Kent
  AddTriple (f1fc16d9-3d3d-47e8-bf42-f080b5e6dc2c)
 Call ID: f1fc16d9-3d3d-47e8-bf42-f080b5e6dc2c
  Args:
    relation: :hasMother
    target: Katharine_Duchess_of_Kent
    source: George_Windsor_Earl_of_St_Andrews
  AddTriple (6b833205-ef04-464e-9ef4-7d59ae52705e)
 Call ID: 6b833205-ef04-464e-9ef4-7d59ae52705e
  Args:
    relation: :hasFather
    target: Prince_Edward_Duke_of_Kent
    source: George_Windsor_Earl_of_St_Andrews
  AssignClass (d837cf72-953c-423e-82c3-f351d8d422bf)
 Call ID: d837cf72-953c-423e-82c3-f351d8d422bf
  Args:
    type: :Man
    source: Lord_Nicholas_Windsor
  AssignClass (5f77102e-f87d-44ee-921d-496bf21c1a34)
 Call ID: 5f77102e-f87d-44ee-921d-496bf21c1a34
  Args:
    source: Lord_Nicholas_Windsor
    type: :Person
  AddTriple (c9e096dc-df1f-4ef0-9672-f1cb7abeeef0)
 Call ID: c9e096dc-df1f-4ef0-9672-f1cb7abeeef0
  Args:
    target: Lord_Nicholas_Windsor
    source: George_Windsor_Earl_of_St_Andrews
    relation: :isSiblingOf
  AssignClass (5b34c21a-add5-4373-8030-3ffb7d132d8b)
 Call ID: 5b34c21a-add5-4373-8030-3ffb7d132d8b
  Args:
    source: William_Worsley_4th_Baronet
    type: :Man
  AssignClass (212a8ac2-6599-49b0-9bd4-274d418ecab7)
 Call ID: 212a8ac2-6599-49b0-9bd4-274d418ecab7
  Args:
    type: :Person
    source: William_Worsley_4th_Baronet
  AddTriple (03e41474-ca2e-47ad-b4d2-068aa17fb577)
 Call ID: 03e41474-ca2e-47ad-b4d2-068aa17fb577
  Args:
    relation: :hasFather
    source: Katharine_Duchess_of_Kent
    target: William_Worsley_4th_Baronet
  Finish (2ef667d1-d50d-4e40-9c10-a8240d9fd49c)
 Call ID: 2ef667d1-d50d-4e40-9c10-a8240d9fd49c
  Args: