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
  AssignClass (b7320b1d-5571-420c-ae57-4a748b9c0f04)
 Call ID: b7320b1d-5571-420c-ae57-4a748b9c0f04
  Args:
    type: :Woman
    source: Amelia_Windsor
  AddLiteral (626c4ed9-594e-435f-9978-cd60b7febf8d)
 Call ID: 626c4ed9-594e-435f-9978-cd60b7febf8d
  Args:
    source: Amelia_Windsor
    literal_value: 1995
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
  AssignClass (35a5d1b2-f0b0-4f69-84d1-536be2cdd52e)
 Call ID: 35a5d1b2-f0b0-4f69-84d1-536be2cdd52e
  Args:
    source: Prince_Edward_Duke_of_Kent
    type: :Man
  AssignClass (6161fd3b-14e0-4e04-80cd-50debc583179)
 Call ID: 6161fd3b-14e0-4e04-80cd-50debc583179
  Args:
    source: George_V
    type: :Man
  AssignClass (baeecf4d-bcd9-489e-9630-6cbd483f4b1f)
 Call ID: baeecf4d-bcd9-489e-9630-6cbd483f4b1f
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (71167b5a-1e6b-4f02-88b6-e01d75281d43)
 Call ID: 71167b5a-1e6b-4f02-88b6-e01d75281d43
  Args:
    type: :Man
    source: George_Windsor_Earl_of_St_Andrews
  AssignClass (5f8b2f79-56a9-4282-afcb-1d95f3efa718)
 Call ID: 5f8b2f79-56a9-4282-afcb-1d95f3efa718
  Args:
    source: Sylvana_Tomaselli
    type: :Woman
  AddTriple (722aa11d-33ed-43ea-9248-ba8b73b592a8)
 Call ID: 722aa11d-33ed-43ea-9248-ba8b73b592a8
  Args:
    target: George_Windsor_Earl_of_St_Andrews
    source: Amelia_Windsor
    relation: :hasFather
  AddTriple (0ac3e875-f81b-4bbe-8491-e08e06bb902e)
 Call ID: 0ac3e875-f81b-4bbe-8491-e08e06bb902e
  Args:
    target: Sylvana_Tomaselli
    relation: :hasMother
    source: Amelia_Windsor
  AddTriple (c34b0c40-4e6c-48df-aebd-16c247c92822)
 Call ID: c34b0c40-4e6c-48df-aebd-16c247c92822
  Args:
    target: Prince_Edward_Duke_of_Kent
    source: George_Windsor_Earl_of_St_Andrews
    relation: :hasFather
  AssignClass (9d44b7bd-e8b9-47d5-a5b1-eb1a6ddaaae9)
 Call ID: 9d44b7bd-e8b9-47d5-a5b1-eb1a6ddaaae9
  Args:
    source: Katharine_Duchess_of_Kent
    type: :Woman
  AddTriple (30f086aa-2fd6-477e-b31b-77df7209bfda)
 Call ID: 30f086aa-2fd6-477e-b31b-77df7209bfda
  Args:
    source: George_Windsor_Earl_of_St_Andrews
    relation: :hasMother
    target: Katharine_Duchess_of_Kent
  AssignClass (1b99edee-d719-47a4-b6d9-ef63ce8b8f70)
 Call ID: 1b99edee-d719-47a4-b6d9-ef63ce8b8f70
  Args:
    type: :Man
    source: Prince_George_Duke_of_Kent
  AssignClass (1dcbc93b-e474-46d9-ac06-26ad6d272e2a)
 Call ID: 1dcbc93b-e474-46d9-ac06-26ad6d272e2a
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    type: :Woman
  AddTriple (8924a769-cd9c-4d44-8605-8dbcc4a02491)
 Call ID: 8924a769-cd9c-4d44-8605-8dbcc4a02491
  Args:
    target: Prince_George_Duke_of_Kent
    source: Prince_Edward_Duke_of_Kent
    relation: :hasFather
  AddTriple (ca714b34-c6c0-4521-8d8e-8234f132d46f)
 Call ID: ca714b34-c6c0-4521-8d8e-8234f132d46f
  Args:
    target: Princess_Marina_of_Greece_and_Denmark
    relation: :hasMother
    source: Prince_Edward_Duke_of_Kent
  AssignClass (0aa0ce02-0e09-4975-8372-f778e828047f)
 Call ID: 0aa0ce02-0e09-4975-8372-f778e828047f
  Args:
    source: Edward_Windsor_Lord_Downpatrick
    type: :Man
  AssignClass (4ddcad15-e578-4362-aef7-d202666e2cb3)
 Call ID: 4ddcad15-e578-4362-aef7-d202666e2cb3
  Args:
    source: Lady_Marina_Windsor
    type: :Woman
  AddTriple (00a389a3-30b6-4112-a82e-b4e5d272be40)
 Call ID: 00a389a3-30b6-4112-a82e-b4e5d272be40
  Args:
    target: Edward_Windsor_Lord_Downpatrick
    source: Amelia_Windsor
    relation: :isSiblingOf
  AddTriple (51027440-ec0d-4c53-9e3e-8a473fdbbdb1)
 Call ID: 51027440-ec0d-4c53-9e3e-8a473fdbbdb1
  Args:
    source: Amelia_Windsor
    relation: :isSiblingOf
    target: Lady_Marina_Windsor
  AssignClass (fb02fb25-de84-43db-9809-29d850e8e8cf)
 Call ID: fb02fb25-de84-43db-9809-29d850e8e8cf
  Args:
    type: :Man
    source: Sir_William_Worsley_4th_Baronet
  AddTriple (81332134-e923-4890-b1f3-8ae1faa06a2d)
 Call ID: 81332134-e923-4890-b1f3-8ae1faa06a2d
  Args:
    relation: :hasFather
    source: Katharine_Duchess_of_Kent
    target: Sir_William_Worsley_4th_Baronet
  AssignClass (8d3b8459-5550-4f91-9633-f7f4cbda59b9)
 Call ID: 8d3b8459-5550-4f91-9633-f7f4cbda59b9
  Args:
    source: Lord_Nicholas_Windsor
    type: :Man
  AddTriple (1b757f51-7752-4c0a-b148-549085ae090a)
 Call ID: 1b757f51-7752-4c0a-b148-549085ae090a
  Args:
    source: Lord_Nicholas_Windsor
    relation: :hasFather
    target: Prince_Edward_Duke_of_Kent
  Finish (c81acc66-52d4-467b-9000-a3aa6a85f2c3)
 Call ID: c81acc66-52d4-467b-9000-a3aa6a85f2c3
  Args: