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
Michael Fergus Bowes-Lyon, 18th and 5th Earl of Strathmore and Kinghorne (7 June 1957 – 27 February 2016), styled Lord Glamis between 1972 and 1987, also known as Mikey Strathmore, was a British Conservative politician, Scots Guards officer and stockbroker.
Early life and education

Strathmore was born on 7 June 1957 in Windsor, the only son of Fergus Bowes-Lyon, later 17th Earl of Strathmore and Kinghorne, and his wife, Mary Pamela McCorquodale.
His paternal grandfather, Lieutenant-Colonel The Honourable Michael Bowes-Lyon, was an elder brother of Queen Elizabeth the Queen Mother, thus making Michael a first cousin once removed of Queen Elizabeth II and Princess Margaret.
Career

After Sandhurst, Strathmore was commissioned in the Scots Guards in 1980.
In 1987, Strathmore succeeded his father as 18th Earl of Strathmore and Kinghorne and inherited Holwick Hall in Teesdale, County Durham, and Glamis Castle, the Queen Mother's girlhood home, in Angus.
After resigning his ministerial post, Strathmore sat on the board of Polypipe from 1994 until it was acquired by IMI plc in 1999.
He also served as president of Boys' Brigade from 1994 to 1999 and as patron of the Friends of the Bowes Museum in County Durham, a position he inherited from the Queen Mother.
Personal life

Strathmore was married three times.
On 14 November 1984, Lord Glamis, as he was then, married Isobel Charlotte Weatherall (born c. 1962), great-granddaughter of Henry Keswick and sister of Percy Weatherall, at St James's Church, Piccadilly, with the Queen Mother in attendance.
Strathmore and Weatherall were separated in 2003 and divorced in 2005.
On 24 November 2005, Strathmore married Damaris Stuart-William, a clinical psychologist.
They had one son:


On 4 August 2012, Strathmore married Karen Baxter (née Orrock), who survived him.
As a hobby, he restored old automobiles and lorries, often featuring in the Strathmore Vintage Vehicle Rally.
In 2002, as the head of the Bowes-Lyon family, he walked behind the Queen Mother's coffin during her funeral procession and attended the private service of committal in the King George VI Memorial Chapel.
Strathmore died of colorectal cancer on 27 February 2016 in London, aged 58.
A memorial service was held at the Church of St Mary the Virgin in Middleton-in-Teesdale, near his County Durham properties, on 12 May and another, attended by Prince Charles, was held at St Martin-in-the-Fields in London on 8 June.



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
  AssignClass (0ca39dce-4ac9-42e7-bf2c-d1089c3c52ad)
 Call ID: 0ca39dce-4ac9-42e7-bf2c-d1089c3c52ad
  Args:
    type: :Man
    source: Michael_Fergus_Bowes-Lyon
  AssignClass (3330e827-c7c8-4ca2-918d-80a717c672d8)
 Call ID: 3330e827-c7c8-4ca2-918d-80a717c672d8
  Args:
    type: :Person
    source: Michael_Fergus_Bowes-Lyon
  AddLiteral (45808a80-95fb-473a-99ea-2553884511f0)
 Call ID: 45808a80-95fb-473a-99ea-2553884511f0
  Args:
    source: Michael_Fergus_Bowes-Lyon
    literal_type: xsd:integer
    literal_value: 1957
    relation: :hasBirthYear
  AddLiteral (e47a1769-01ea-4b89-bc48-0124df130360)
 Call ID: e47a1769-01ea-4b89-bc48-0124df130360
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2016
    source: Michael_Fergus_Bowes-Lyon
  AddLiteral (7099cb26-082d-4640-b3c5-7990063edf3d)
 Call ID: 7099cb26-082d-4640-b3c5-7990063edf3d
  Args:
    source: Michael_Fergus_Bowes-Lyon
    literal_value: Mikey Strathmore
    literal_type: xsd:string
    relation: :alsoKnownAs
  AssignClass (ea122b48-41a1-423c-837b-64193092fb54)
 Call ID: ea122b48-41a1-423c-837b-64193092fb54
  Args:
    type: :Man
    source: Fergus_Bowes-Lyon
  AssignClass (5b2c5e10-a85d-4507-add8-954af24e40f8)
 Call ID: 5b2c5e10-a85d-4507-add8-954af24e40f8
  Args:
    type: :Person
    source: Fergus_Bowes-Lyon
  AddTriple (e805eb82-fa15-4feb-b58e-acef7f207421)
 Call ID: e805eb82-fa15-4feb-b58e-acef7f207421
  Args:
    relation: :hasFather
    target: Fergus_Bowes-Lyon
    source: Michael_Fergus_Bowes-Lyon
  AssignClass (261454f3-0ff9-4c03-ad3b-7d1ce1f55d06)
 Call ID: 261454f3-0ff9-4c03-ad3b-7d1ce1f55d06
  Args:
    type: :Woman
    source: Mary_Pamela_McCorquodale
  AssignClass (c8494efc-e0f8-4261-b103-a6c6d3de7b77)
 Call ID: c8494efc-e0f8-4261-b103-a6c6d3de7b77
  Args:
    type: :Person
    source: Mary_Pamela_McCorquodale
  AddTriple (88e686fd-8e5f-4056-91ce-7557980dc8d4)
 Call ID: 88e686fd-8e5f-4056-91ce-7557980dc8d4
  Args:
    target: Mary_Pamela_McCorquodale
    relation: :hasMother
    source: Michael_Fergus_Bowes-Lyon
  AssignClass (9b78ad6a-967e-4b6b-902e-127daae23c0e)
 Call ID: 9b78ad6a-967e-4b6b-902e-127daae23c0e
  Args:
    type: :Man
    source: Michael_Bowes-Lyon_Grandfather
  AssignClass (6bd76dd3-ad9b-4bb6-851d-bfa02f59bdcf)
 Call ID: 6bd76dd3-ad9b-4bb6-851d-bfa02f59bdcf
  Args:
    type: :Person
    source: Michael_Bowes-Lyon_Grandfather
  AddTriple (f8010415-cc7f-465f-b4e9-3cca93961553)
 Call ID: f8010415-cc7f-465f-b4e9-3cca93961553
  Args:
    source: Fergus_Bowes-Lyon
    target: Michael_Bowes-Lyon_Grandfather
    relation: :hasFather
  AssignClass (5b8121f8-e8e1-46bd-8584-f67c21440fca)
 Call ID: 5b8121f8-e8e1-46bd-8584-f67c21440fca
  Args:
    type: :Woman
    source: Queen_Elizabeth_The_Queen_Mother
  AssignClass (f3f0225e-fe0d-4515-af67-76529900a3c6)
 Call ID: f3f0225e-fe0d-4515-af67-76529900a3c6
  Args:
    type: :Person
    source: Queen_Elizabeth_The_Queen_Mother
  AddTriple (0c196f3c-5bd0-4cce-a245-df30721f04c3)
 Call ID: 0c196f3c-5bd0-4cce-a245-df30721f04c3
  Args:
    source: Queen_Elizabeth_The_Queen_Mother
    target: Michael_Bowes-Lyon_Grandfather
    relation: :isSisterOf
  AssignClass (f2207430-54f3-4ca7-92db-2887104d2764)
 Call ID: f2207430-54f3-4ca7-92db-2887104d2764
  Args:
    type: :Woman
    source: Isobel_Charlotte_Weatherall
  AssignClass (1400012e-aacf-4be3-a5c3-fc0426a8e809)
 Call ID: 1400012e-aacf-4be3-a5c3-fc0426a8e809
  Args:
    type: :Person
    source: Isobel_Charlotte_Weatherall
  AddLiteral (2f9739c2-d209-4438-aad6-740df766b441)
 Call ID: 2f9739c2-d209-4438-aad6-740df766b441
  Args:
    source: Michael_Fergus_Bowes-Lyon
    literal_type: xsd:integer
    literal_value: 1984
    relation: :hasMarriageYear
  AddTriple (f6ab7ef3-bac4-48c0-a994-6e2a6123f3b7)
 Call ID: f6ab7ef3-bac4-48c0-a994-6e2a6123f3b7
  Args:
    source: Michael_Fergus_Bowes-Lyon
    target: Isobel_Charlotte_Weatherall
    relation: :hasRelation
  AssignClass (37288b9a-2a82-43e7-a1ff-8ff6ce069392)
 Call ID: 37288b9a-2a82-43e7-a1ff-8ff6ce069392
  Args:
    type: :Woman
    source: Damaris_Stuart-William
  AssignClass (f3a424c7-9e32-416e-8d1b-ed0f3609b41f)
 Call ID: f3a424c7-9e32-416e-8d1b-ed0f3609b41f
  Args:
    type: :Person
    source: Damaris_Stuart-William
  AddLiteral (f65cb0d6-5cfa-4c38-8875-c1375dc53943)
 Call ID: f65cb0d6-5cfa-4c38-8875-c1375dc53943
  Args:
    relation: :hasMarriageYear
    literal_value: 2005
    literal_type: xsd:integer
    source: Michael_Fergus_Bowes-Lyon
  AddTriple (4e83990c-f6de-44fc-962d-c2ede9fb50e2)
 Call ID: 4e83990c-f6de-44fc-962d-c2ede9fb50e2
  Args:
    source: Michael_Fergus_Bowes-Lyon
    relation: :hasRelation
    target: Damaris_Stuart-William
  AssignClass (09a04de3-d7f6-478d-ad6d-a2cc0038fc8e)
 Call ID: 09a04de3-d7f6-478d-ad6d-a2cc0038fc8e
  Args:
    type: :Woman
    source: Karen_Baxter
  AssignClass (eddef1ad-3408-44ed-be06-b4ad1dab676c)
 Call ID: eddef1ad-3408-44ed-be06-b4ad1dab676c
  Args:
    type: :Person
    source: Karen_Baxter
  AddLiteral (d6397895-f9a1-4dfa-93f9-d157b35e01f3)
 Call ID: d6397895-f9a1-4dfa-93f9-d157b35e01f3
  Args:
    source: Michael_Fergus_Bowes-Lyon
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 2012
  AddTriple (ea5e402e-485e-4704-a6ad-939d66d11d67)
 Call ID: ea5e402e-485e-4704-a6ad-939d66d11d67
  Args:
    relation: :hasRelation
    target: Karen_Baxter
    source: Michael_Fergus_Bowes-Lyon
  AssignClass (b89cd5f1-4cfa-4bc5-b7ab-80d58221e00d)
 Call ID: b89cd5f1-4cfa-4bc5-b7ab-80d58221e00d
  Args:
    type: :Man
    source: Henry_Keswick
  AssignClass (3b37c90f-fa95-4d7d-bd52-7ea319f21028)
 Call ID: 3b37c90f-fa95-4d7d-bd52-7ea319f21028
  Args:
    type: :Person
    source: Henry_Keswick
  AssignClass (e2b4b333-e8c8-4430-a130-e0dc1b13a216)
 Call ID: e2b4b333-e8c8-4430-a130-e0dc1b13a216
  Args:
    type: :Man
    source: Percy_Weatherall
  AssignClass (e7b3bf21-ff81-498d-b400-0c2c1284b519)
 Call ID: e7b3bf21-ff81-498d-b400-0c2c1284b519
  Args:
    type: :Person
    source: Percy_Weatherall
  AddTriple (11ef83b4-18b2-499b-8907-1e905ea1a45c)
 Call ID: 11ef83b4-18b2-499b-8907-1e905ea1a45c
  Args:
    source: Percy_Weatherall
    relation: :isBrotherOf
    target: Isobel_Charlotte_Weatherall
  Finish (3c930eac-ba91-4df4-a2ba-5bf217afa71f)
 Call ID: 3c930eac-ba91-4df4-a2ba-5bf217afa71f
  Args: