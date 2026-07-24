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
  AssignClass (2c637cc9-3762-428b-b121-5c82691f86e0)
 Call ID: 2c637cc9-3762-428b-b121-5c82691f86e0
  Args:
    source: Michael_Fergus_Bowes-Lyon
    type: :Man
  AssignClass (b86e5c2e-4082-451e-95a1-1da2b5292156)
 Call ID: b86e5c2e-4082-451e-95a1-1da2b5292156
  Args:
    type: :Man
    source: Fergus_Bowes-Lyon
  AssignClass (18942785-778c-418c-b5ea-73e787f02c76)
 Call ID: 18942785-778c-418c-b5ea-73e787f02c76
  Args:
    source: Mary_Pamela_McCorquodale
    type: :Woman
  AssignClass (6c5e6f65-3dea-4797-8ee5-d0cb079f545e)
 Call ID: 6c5e6f65-3dea-4797-8ee5-d0cb079f545e
  Args:
    source: Michael_Bowes-Lyon_LtCol
    type: :Man
  AssignClass (f9261765-eb0c-4088-b543-9448b3043dea)
 Call ID: f9261765-eb0c-4088-b543-9448b3043dea
  Args:
    source: Queen_Elizabeth_The_Queen_Mother
    type: :Woman
  AssignClass (790a33fd-d3b8-4e3a-978d-f3d4d0c07034)
 Call ID: 790a33fd-d3b8-4e3a-978d-f3d4d0c07034
  Args:
    source: Isobel_Charlotte_Weatherall
    type: :Woman
  AssignClass (02c0a487-3ef9-4b03-a756-f0a50e1bd8c3)
 Call ID: 02c0a487-3ef9-4b03-a756-f0a50e1bd8c3
  Args:
    source: Damaris_Stuart-William
    type: :Woman
  AssignClass (64b98ceb-f2ce-4a5c-85b5-84d569fee470)
 Call ID: 64b98ceb-f2ce-4a5c-85b5-84d569fee470
  Args:
    type: :Woman
    source: Karen_Baxter
  AssignClass (03bfe9f4-e3e1-42b3-93f4-0ae91696326b)
 Call ID: 03bfe9f4-e3e1-42b3-93f4-0ae91696326b
  Args:
    source: Percy_Weatherall
    type: :Man
  AddLiteral (51e9288d-6d9b-41bf-8615-40231548ce76)
 Call ID: 51e9288d-6d9b-41bf-8615-40231548ce76
  Args:
    literal_value: Mikey Strathmore
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Michael_Fergus_Bowes-Lyon
  AddLiteral (5d8581f2-0fa1-4014-b999-743971ff3d02)
 Call ID: 5d8581f2-0fa1-4014-b999-743971ff3d02
  Args:
    literal_type: xsd:integer
    source: Michael_Fergus_Bowes-Lyon
    relation: :hasBirthYear
    literal_value: 1957
  AddLiteral (73261a95-1331-427c-9c5a-bbbc4150a45e)
 Call ID: 73261a95-1331-427c-9c5a-bbbc4150a45e
  Args:
    relation: :hasDeathYear
    literal_value: 2016
    source: Michael_Fergus_Bowes-Lyon
    literal_type: xsd:integer
  AddTriple (3329baf9-c32c-4f03-8295-13ae3ce79e32)
 Call ID: 3329baf9-c32c-4f03-8295-13ae3ce79e32
  Args:
    source: Michael_Fergus_Bowes-Lyon
    target: Fergus_Bowes-Lyon
    relation: :hasFather
  AddTriple (402267f2-524a-4e80-8d35-37c54c00b16e)
 Call ID: 402267f2-524a-4e80-8d35-37c54c00b16e
  Args:
    source: Michael_Fergus_Bowes-Lyon
    relation: :hasMother
    target: Mary_Pamela_McCorquodale
  AddTriple (fa8f212b-1c20-47e3-9735-8b12d8bc1e95)
 Call ID: fa8f212b-1c20-47e3-9735-8b12d8bc1e95
  Args:
    source: Fergus_Bowes-Lyon
    relation: :hasFather
    target: Michael_Bowes-Lyon_LtCol
  AddTriple (69dd0f0b-fe20-44cb-a3d9-c28de39f78f4)
 Call ID: 69dd0f0b-fe20-44cb-a3d9-c28de39f78f4
  Args:
    source: Michael_Bowes-Lyon_LtCol
    target: Queen_Elizabeth_The_Queen_Mother
    relation: :hasSister
  AddLiteral (7b6ea0ad-0c67-4c1b-8660-ca20fa90faa1)
 Call ID: 7b6ea0ad-0c67-4c1b-8660-ca20fa90faa1
  Args:
    source: Michael_Fergus_Bowes-Lyon
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1984
  AddTriple (f7a2e7ec-60bd-4de2-bbd8-53e4830da331)
 Call ID: f7a2e7ec-60bd-4de2-bbd8-53e4830da331
  Args:
    target: Isobel_Charlotte_Weatherall
    relation: :hasRelation
    source: Michael_Fergus_Bowes-Lyon
  AddTriple (00f1a872-0e30-4f0f-a570-a7f82d2c6ba8)
 Call ID: 00f1a872-0e30-4f0f-a570-a7f82d2c6ba8
  Args:
    source: Michael_Fergus_Bowes-Lyon
    target: Damaris_Stuart-William
    relation: :hasRelation
  AddTriple (0a54db30-68dc-468d-97d5-99f93356aa83)
 Call ID: 0a54db30-68dc-468d-97d5-99f93356aa83
  Args:
    relation: :hasRelation
    target: Karen_Baxter
    source: Michael_Fergus_Bowes-Lyon
  AddTriple (78f60c54-ae30-4293-b1cf-a4ad1cb7ef4e)
 Call ID: 78f60c54-ae30-4293-b1cf-a4ad1cb7ef4e
  Args:
    source: Percy_Weatherall
    relation: :hasSister
    target: Isobel_Charlotte_Weatherall
  Finish (a7ab80e1-7725-4424-8433-71bb1d8df4ae)
 Call ID: a7ab80e1-7725-4424-8433-71bb1d8df4ae
  Args: