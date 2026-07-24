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
  AssignClass (49a7c4ab-6342-4e3b-8ca2-bed66354bbab)
 Call ID: 49a7c4ab-6342-4e3b-8ca2-bed66354bbab
  Args:
    type: :Woman
    source: Amelia_Windsor
  AssignClass (04fa3fd5-3852-47e6-bfab-1d8931da8840)
 Call ID: 04fa3fd5-3852-47e6-bfab-1d8931da8840
  Args:
    type: :Person
    source: Amelia_Windsor
  AddLiteral (405f1df4-39d0-4481-80f2-42c13436ac3e)
 Call ID: 405f1df4-39d0-4481-80f2-42c13436ac3e
  Args:
    literal_value: 1995
    source: Amelia_Windsor
    literal_type: xsd:string
    relation: :hasBirthYear
  AssignClass (1f43533d-5c35-433a-ada7-30d1e4af39df)
 Call ID: 1f43533d-5c35-433a-ada7-30d1e4af39df
  Args:
    type: :Man
    source: Prince_Edward_Duke_of_Kent
  AssignClass (186a8fbf-ce2d-4228-b20d-5ff65f5874a2)
 Call ID: 186a8fbf-ce2d-4228-b20d-5ff65f5874a2
  Args:
    type: :Ancestor
    source: Prince_Edward_Duke_of_Kent
  AssignClass (70eaefc4-7e47-47e5-a1aa-12189fbeae6f)
 Call ID: 70eaefc4-7e47-47e5-a1aa-12189fbeae6f
  Args:
    type: :Man
    source: George_V
  AssignClass (f0dfcf84-4f88-4b85-b043-10a64336e04f)
 Call ID: f0dfcf84-4f88-4b85-b043-10a64336e04f
  Args:
    type: :Ancestor
    source: George_V
  AssignClass (971e4372-1e5f-4242-b4fa-b259ccf146c8)
 Call ID: 971e4372-1e5f-4242-b4fa-b259ccf146c8
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (fa235703-5965-425e-a532-1fb7cc6be5ad)
 Call ID: fa235703-5965-425e-a532-1fb7cc6be5ad
  Args:
    type: :Ancestor
    source: Queen_Mary
  AddTriple (a58af2a0-c3a3-4ce2-a6c2-87819d7c1b5a)
 Call ID: a58af2a0-c3a3-4ce2-a6c2-87819d7c1b5a
  Args:
    relation: :isChildOf
    target: Prince_Edward_Duke_of_Kent
    source: Amelia_Windsor
  AssignClass (b7b27462-58f9-43a8-85f0-2bed003a5305)
 Call ID: b7b27462-58f9-43a8-85f0-2bed003a5305
  Args:
    type: :Man
    source: George_Windsor_Earl_of_St_Andrews
  AssignClass (9d05c1dd-c95f-47fa-a122-70a1b9a26ba9)
 Call ID: 9d05c1dd-c95f-47fa-a122-70a1b9a26ba9
  Args:
    type: :Person
    source: George_Windsor_Earl_of_St_Andrews
  AssignClass (ccecea6d-85db-4a27-ada6-1d541d07a0e8)
 Call ID: ccecea6d-85db-4a27-ada6-1d541d07a0e8
  Args:
    type: :Woman
    source: Sylvana_Tomaselli
  AssignClass (14108c01-a952-4203-9269-ff77fa27c8a2)
 Call ID: 14108c01-a952-4203-9269-ff77fa27c8a2
  Args:
    type: :Person
    source: Sylvana_Tomaselli
  AddTriple (f9b74b27-f5e9-4f7b-894f-946d1412663b)
 Call ID: f9b74b27-f5e9-4f7b-894f-946d1412663b
  Args:
    source: Amelia_Windsor
    relation: :hasFather
    target: George_Windsor_Earl_of_St_Andrews
  AddTriple (0868cbf8-f532-491b-bda2-1f41b2b24778)
 Call ID: 0868cbf8-f532-491b-bda2-1f41b2b24778
  Args:
    relation: :hasMother
    target: Sylvana_Tomaselli
    source: Amelia_Windsor
  AssignClass (ec82873d-4ba3-4378-9e02-5ad58956c75a)
 Call ID: ec82873d-4ba3-4378-9e02-5ad58956c75a
  Args:
    type: :Man
    source: Edward_Windsor_Lord_Downpatrick
  AssignClass (48f2d537-c49a-45ae-bf9d-96fae2ce1b8b)
 Call ID: 48f2d537-c49a-45ae-bf9d-96fae2ce1b8b
  Args:
    type: :Person
    source: Edward_Windsor_Lord_Downpatrick
  AssignClass (b14aa84e-e8f8-43ea-ae7e-0df474f669a1)
 Call ID: b14aa84e-e8f8-43ea-ae7e-0df474f669a1
  Args:
    type: :Woman
    source: Lady_Marina_Windsor
  AssignClass (00bd3201-dd86-4252-957d-34505d3c863e)
 Call ID: 00bd3201-dd86-4252-957d-34505d3c863e
  Args:
    type: :Person
    source: Lady_Marina_Windsor
  AddTriple (5d999d60-0ea7-4173-9f6d-3df788b3cb36)
 Call ID: 5d999d60-0ea7-4173-9f6d-3df788b3cb36
  Args:
    relation: :isSiblingOf
    target: Edward_Windsor_Lord_Downpatrick
    source: Amelia_Windsor
  AddTriple (ff2ef32c-394c-42b2-b55a-b03e1662f00d)
 Call ID: ff2ef32c-394c-42b2-b55a-b03e1662f00d
  Args:
    relation: :isSiblingOf
    target: Lady_Marina_Windsor
    source: Amelia_Windsor
  AssignClass (9d270623-dab0-4141-8cff-6f368a709ecc)
 Call ID: 9d270623-dab0-4141-8cff-6f368a709ecc
  Args:
    type: :Man
    source: Prince_George_Duke_of_Kent
  AssignClass (242fced4-f8ae-4b1c-8bd5-a6e889ae4043)
 Call ID: 242fced4-f8ae-4b1c-8bd5-a6e889ae4043
  Args:
    type: :Ancestor
    source: Prince_George_Duke_of_Kent
  AssignClass (5790c6b6-106c-4e36-82b5-f1e899b86204)
 Call ID: 5790c6b6-106c-4e36-82b5-f1e899b86204
  Args:
    type: :Woman
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (280ba576-024c-464c-abd1-455d186369e5)
 Call ID: 280ba576-024c-464c-abd1-455d186369e5
  Args:
    type: :Ancestor
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (7f1bff39-3a09-4d26-a1a1-c2d0ccc564a0)
 Call ID: 7f1bff39-3a09-4d26-a1a1-c2d0ccc564a0
  Args:
    type: :Woman
    source: Mary_of_Teck
  AssignClass (9cfe1951-8a0e-4f2c-9e17-82e2d852ca45)
 Call ID: 9cfe1951-8a0e-4f2c-9e17-82e2d852ca45
  Args:
    type: :Ancestor
    source: Mary_of_Teck
  AssignClass (ef91a012-d3ac-43d6-abfc-9e9f956bdeb4)
 Call ID: ef91a012-d3ac-43d6-abfc-9e9f956bdeb4
  Args:
    type: :Woman
    source: Katharine_Duchess_of_Kent
  AssignClass (62212cc9-f623-4596-9f25-63da13f4a8a7)
 Call ID: 62212cc9-f623-4596-9f25-63da13f4a8a7
  Args:
    type: :Person
    source: Katharine_Duchess_of_Kent
  AssignClass (560d4ed3-f998-4e9b-add9-e9d25a8f184a)
 Call ID: 560d4ed3-f998-4e9b-add9-e9d25a8f184a
  Args:
    type: :Man
    source: Sir_William_Worsley_4th_Baronet
  AssignClass (2df6f9d4-0def-4068-ab72-d6d6042f004c)
 Call ID: 2df6f9d4-0def-4068-ab72-d6d6042f004c
  Args:
    type: :Ancestor
    source: Sir_William_Worsley_4th_Baronet
  AddTriple (38fc045c-cdde-4ae6-80d3-35bf6aec5919)
 Call ID: 38fc045c-cdde-4ae6-80d3-35bf6aec5919
  Args:
    target: Prince_Edward_Duke_of_Kent
    relation: :isFatherOf
    source: Prince_George_Duke_of_Kent
  AddTriple (493970bf-28ee-4555-a826-76a2ef242c7b)
 Call ID: 493970bf-28ee-4555-a826-76a2ef242c7b
  Args:
    relation: :isMotherOf
    target: Prince_Edward_Duke_of_Kent
    source: Princess_Marina_of_Greece_and_Denmark
  AddTriple (045a4158-70a4-4b4f-be68-2cbd8c44f69b)
 Call ID: 045a4158-70a4-4b4f-be68-2cbd8c44f69b
  Args:
    relation: :isMotherOf
    target: George_Windsor_Earl_of_St_Andrews
    source: Katharine_Duchess_of_Kent
  AddTriple (c3f0798e-fea9-4a21-b5bf-d99bc95be890)
 Call ID: c3f0798e-fea9-4a21-b5bf-d99bc95be890
  Args:
    source: Sir_William_Worsley_4th_Baronet
    relation: :isFatherOf
    target: Katharine_Duchess_of_Kent
  AssignClass (8b85dae4-ea5f-4ffd-afb3-dc054c56c37e)
 Call ID: 8b85dae4-ea5f-4ffd-afb3-dc054c56c37e
  Args:
    type: :Man
    source: Lord_Nicholas_Windsor
  AssignClass (350458a8-ab62-4836-a55a-4583fd918bf0)
 Call ID: 350458a8-ab62-4836-a55a-4583fd918bf0
  Args:
    type: :Person
    source: Lord_Nicholas_Windsor
  AddTriple (65cebd14-335a-42ca-b637-3b1aaf1ebfad)
 Call ID: 65cebd14-335a-42ca-b637-3b1aaf1ebfad
  Args:
    source: George_Windsor_Earl_of_St_Andrews
    relation: :isSiblingOf
    target: Lord_Nicholas_Windsor
  Finish (fb1fd73d-8ca2-4882-9099-74e2fa7faba8)
 Call ID: fb1fd73d-8ca2-4882-9099-74e2fa7faba8
  Args: