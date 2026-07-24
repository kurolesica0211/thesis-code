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
Prince Wolfgang of Hesse (Wolfgang Moritz Prinz von Hessen; 6 November 1896 – 12 July 1989) was the district administrator of Obertaunuskreis from 1933 to 1945.
Wolfgang was born at Castle Rumpenheim, Offenbach am Main, the fourth son of Prince Frederick Charles of Hesse (1868–1940) and Princess Margaret of Prussia (1872–1954).
His maternal uncle was the German Emperor Willhelm II.
In World War I, Wolfgang served as an officer in the command of Field Marshal August von Mackensen.
Towards the end of the war, Wolfgang's father Frederick Charles of Hesse was selected by the Central Powers as a prospective King of Finland on 9 October 1918, to replace his first cousin once removed, the deposed Russian emperor, Nicholas II, who was titled Grand Duke of Finland.
Wolfgang was designated heir, in preference to his elder twin brother Philipp to ensure the separation of the thrones of Hesse and Finland.
However, Frederick Charles renounced his candidature on 14 December 1918, and the title was never actually held by the family.
Wolfgang married on 17 September 1924 Princess Marie Alexandra of Baden (1902–1944), daughter of Prince Maximilian of Baden and Princess Marie Louise of Hanover; they had no children.
He joined the NSDAP and the SA in December 1933, and was appointed Landrat (district administrator) of Obertaunuskreis, a landkreis in the state of Hesse, serving in that capacity until the end of  World War II.



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
  AssignClass (fa70fb5e-b5b6-48ae-8904-e393cd1be42b)
 Call ID: fa70fb5e-b5b6-48ae-8904-e393cd1be42b
  Args:
    type: :Man
    source: Wolfgang_of_Hesse
  AssignClass (f23ff4b8-08f2-4568-8971-2a9cc2048092)
 Call ID: f23ff4b8-08f2-4568-8971-2a9cc2048092
  Args:
    type: :Person
    source: Wolfgang_of_Hesse
  AddLiteral (80b0d017-280c-4830-9996-b53019cd56fa)
 Call ID: 80b0d017-280c-4830-9996-b53019cd56fa
  Args:
    literal_value: 1896
    literal_type: xsd:integer
    source: Wolfgang_of_Hesse
    relation: :hasBirthYear
  AddLiteral (34097341-d16d-4dd3-ac58-b3c7666b2351)
 Call ID: 34097341-d16d-4dd3-ac58-b3c7666b2351
  Args:
    literal_type: xsd:integer
    literal_value: 1989
    relation: :hasDeathYear
    source: Wolfgang_of_Hesse
  AddLiteral (38d037a8-ea8d-484a-b829-55e5d6fa2ae2)
 Call ID: 38d037a8-ea8d-484a-b829-55e5d6fa2ae2
  Args:
    literal_value: Wolfgang Moritz Prinz von Hessen
    literal_type: xsd:string
    source: Wolfgang_of_Hesse
    relation: :alsoKnownAs
  AssignClass (e30695cb-0f16-450a-8e31-3e12042df1bf)
 Call ID: e30695cb-0f16-450a-8e31-3e12042df1bf
  Args:
    type: :Man
    source: Frederick_Charles_of_Hesse
  AssignClass (c3da25bb-bba3-4ae8-94c6-a1c1646de63b)
 Call ID: c3da25bb-bba3-4ae8-94c6-a1c1646de63b
  Args:
    type: :Person
    source: Frederick_Charles_of_Hesse
  AddLiteral (3d29ba68-1939-4bb2-bf8d-3fd4d9ea2d2a)
 Call ID: 3d29ba68-1939-4bb2-bf8d-3fd4d9ea2d2a
  Args:
    relation: :hasBirthYear
    source: Frederick_Charles_of_Hesse
    literal_type: xsd:integer
    literal_value: 1868
  AddLiteral (14a84e9a-fe4c-4d58-a5e0-d307f7ef567c)
 Call ID: 14a84e9a-fe4c-4d58-a5e0-d307f7ef567c
  Args:
    literal_value: 1940
    literal_type: xsd:integer
    source: Frederick_Charles_of_Hesse
    relation: :hasDeathYear
  AddTriple (59798e6d-2e28-4970-84af-bdd69894bed3)
 Call ID: 59798e6d-2e28-4970-84af-bdd69894bed3
  Args:
    target: Frederick_Charles_of_Hesse
    source: Wolfgang_of_Hesse
    relation: :hasFather
  AssignClass (31a820ac-7daf-4208-98cf-f7004c675f6c)
 Call ID: 31a820ac-7daf-4208-98cf-f7004c675f6c
  Args:
    type: :Woman
    source: Margaret_of_Prussia
  AssignClass (fb491d90-9146-4407-80ec-354248c47051)
 Call ID: fb491d90-9146-4407-80ec-354248c47051
  Args:
    type: :Person
    source: Margaret_of_Prussia
  AddLiteral (61cf480f-fc38-40f7-aabd-586d62512ea1)
 Call ID: 61cf480f-fc38-40f7-aabd-586d62512ea1
  Args:
    source: Margaret_of_Prussia
    relation: :hasBirthYear
    literal_value: 1872
    literal_type: xsd:integer
  AddLiteral (80811f80-48de-495e-8ad1-1ca6aa174b78)
 Call ID: 80811f80-48de-495e-8ad1-1ca6aa174b78
  Args:
    literal_type: xsd:integer
    literal_value: 1954
    relation: :hasDeathYear
    source: Margaret_of_Prussia
  AddTriple (ff246eb5-6d97-4a3f-8498-0a152c23e77b)
 Call ID: ff246eb5-6d97-4a3f-8498-0a152c23e77b
  Args:
    source: Wolfgang_of_Hesse
    relation: :hasMother
    target: Margaret_of_Prussia
  AssignClass (eb11a1df-7cdb-4142-9943-57cbb311c4b2)
 Call ID: eb11a1df-7cdb-4142-9943-57cbb311c4b2
  Args:
    type: :Man
    source: Philipp_of_Hesse
  AssignClass (12a732ef-0b9a-46dd-94df-d7ec77f5d49b)
 Call ID: 12a732ef-0b9a-46dd-94df-d7ec77f5d49b
  Args:
    type: :Person
    source: Philipp_of_Hesse
  AddTriple (fd67713f-87ce-4f5a-a9d5-629513f81215)
 Call ID: fd67713f-87ce-4f5a-a9d5-629513f81215
  Args:
    target: Philipp_of_Hesse
    source: Wolfgang_of_Hesse
    relation: :isSiblingOf
  AssignClass (5489dabf-fa0d-4464-bdf9-d87b061d5e18)
 Call ID: 5489dabf-fa0d-4464-bdf9-d87b061d5e18
  Args:
    type: :Woman
    source: Marie_Alexandra_of_Baden
  AssignClass (7a20cc59-5f9e-4173-bd8c-86859a6d1a41)
 Call ID: 7a20cc59-5f9e-4173-bd8c-86859a6d1a41
  Args:
    type: :Person
    source: Marie_Alexandra_of_Baden
  AddLiteral (42190001-d99e-4b66-acd2-552b8d74d437)
 Call ID: 42190001-d99e-4b66-acd2-552b8d74d437
  Args:
    literal_value: 1902
    literal_type: xsd:integer
    source: Marie_Alexandra_of_Baden
    relation: :hasBirthYear
  AddLiteral (15240fac-e17d-4877-8d05-f14cc394d90f)
 Call ID: 15240fac-e17d-4877-8d05-f14cc394d90f
  Args:
    source: Marie_Alexandra_of_Baden
    relation: :hasDeathYear
    literal_value: 1944
    literal_type: xsd:integer
  AddLiteral (07f2ba7e-abf8-40a1-8883-a22be3421931)
 Call ID: 07f2ba7e-abf8-40a1-8883-a22be3421931
  Args:
    literal_type: xsd:integer
    literal_value: 1924
    relation: :hasMarriageYear
    source: Wolfgang_of_Hesse
  AddTriple (d6a872ae-4978-4caf-9ebf-f1e24729f260)
 Call ID: d6a872ae-4978-4caf-9ebf-f1e24729f260
  Args:
    target: Marie_Alexandra_of_Baden
    source: Wolfgang_of_Hesse
    relation: :hasRelation
  AssignClass (24353686-adff-4db4-b386-eefa323b5c04)
 Call ID: 24353686-adff-4db4-b386-eefa323b5c04
  Args:
    type: :Man
    source: Maximilian_of_Baden
  AssignClass (cebf832b-2ed1-423c-a099-cb4d86466573)
 Call ID: cebf832b-2ed1-423c-a099-cb4d86466573
  Args:
    type: :Person
    source: Maximilian_of_Baden
  AssignClass (3b128984-6617-4015-a5dc-7fa8d229717c)
 Call ID: 3b128984-6617-4015-a5dc-7fa8d229717c
  Args:
    type: :Woman
    source: Marie_Louise_of_Hanover
  AssignClass (763f1f1c-db5f-44cd-b3be-6aa38424c092)
 Call ID: 763f1f1c-db5f-44cd-b3be-6aa38424c092
  Args:
    type: :Person
    source: Marie_Louise_of_Hanover
  AddTriple (43583185-e872-47d8-9fe8-48fa4e1711f8)
 Call ID: 43583185-e872-47d8-9fe8-48fa4e1711f8
  Args:
    target: Maximilian_of_Baden
    relation: :hasFather
    source: Marie_Alexandra_of_Baden
  AddTriple (9042184c-78cf-442b-b544-c5d45ec06e3c)
 Call ID: 9042184c-78cf-442b-b544-c5d45ec06e3c
  Args:
    target: Marie_Louise_of_Hanover
    source: Marie_Alexandra_of_Baden
    relation: :hasMother
  Finish (b420886a-dea5-42a7-b4b2-49e8cdb0a6e9)
 Call ID: b420886a-dea5-42a7-b4b2-49e8cdb0a6e9
  Args: