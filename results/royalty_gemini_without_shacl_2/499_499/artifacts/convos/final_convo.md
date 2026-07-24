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
Pedro Luiz of Orléans-Braganza (Pedro Luiz Maria José Miguel Gabriel Rafael Gonzaga; 12 January 1983 – 1 June 2009) was a Brazilian prince of the House of Orléans-Braganza.
He was the eldest grandson of Prince Pedro Henrique of Orléans-Braganza and Princess Maria Elisabeth of Bavaria.
A great-great-grandson of Princess Isabel and her consort Gaston of Orléans, Count of Eu, as well as of Emperor Pedro II and Empress Teresa Cristina, Pedro Luiz occupied a prominent place in the line of succession claimed by Brazilian monarchists.
His childless uncle, Bertrand of Orléans-Braganza, is one of the two current claimants to the defunct Brazilian throne, with Pedro Luiz’s father regarded as Bertrand’s immediate successor.
Because of this position, some supporters of Brazilian monarchism expected Pedro Luiz to eventually become the imperial claimant.
Family

Prince Pedro Luiz was born on 12 January 1983 in Rio de Janeiro, the elder of the two sons of Prince António of Orléans-Braganza and his Belgian wife, Princess Christine of Ligne.
His name in full was Pedro Luiz Maria José Miguel Gabriel Rafael Gonzaga de Orleans e Bragança.
His paternal grandparents were Prince Pedro Henrique of Orléans-Braganza, one of two claimants to be head of the Brazilian Imperial House, and Princess Maria Elisabeth of Bavaria.
His maternal grandparents were Antoine, 13th Prince of Ligne, and Princess Alix of Luxembourg.
His mother's family, the House of Ligne, is one of the oldest and most prominent Wallonian noble families still extant in Belgium.
Christine is a niece of Grand Duke Jean, who reigned in Luxembourg until his abdication in 2000.
By 2009, his father's two elder brothers, Prince Luiz and Prince Bertrand, were unmarried and had no offspring.
His father António was therefore heir to the claim after his older siblings, and Pedro would, in due course, have been a claimant to the traditional headship of the Imperial House of Brazil, and the nominal Brazilian crown.
Pedro descended from all monarchs of the Kingdom of Portugal, including Dom João VI of Portugal, Brazil and the Algarves, and the later monarchs of independent Brazil, emperors Dom Pedro
I and Dom Pedro II.
Career

Pedro Luiz held dual Brazilian-Belgian citizenship and was fluent in Portuguese, English and French.
Luiz and Bertrand, known for their political beliefs, were denounced not only by some monarchists, but also by four of their own younger brothers, who tried unsuccessfully to convince them to renounce their traditional claims to the throne in favour of their brother António, and the young Pedro Luiz.
Then only ten years old, Pedro Luiz was seen beside his father during the monarchist restoration campaign.
Luiz and Bertrand believed that Pedro Luiz would be a better choice if the monarchy were to be reinstated by the Brazilian people.
In 1999 he became honorary president of Brazil's Monarchist Youth, and also held the Grand Crosses of the Order of Pedro I and of the Order of the Rose.


Pedro Luiz had expressed some opinions about Brazilian politics aside from the monarchy.
Regarding the government of President Luiz Inácio Lula da Silva he stated, "I am very pleased with the economic performance of Brazil, all derived from the policy of Lula da Silva.
Pedro Luiz was considered by many Brazilian monarchists as the prince that gathered "all the hopes and aspirations " due to the "vigor of youth and the seriousness of his character".
Duarte Pio, Duke of Bragança and heir of the abolished Portuguese crown, affirmed: " is a very intelligent person.
"


Death

Luiz was killed in the crash of Air France Flight 447 on 1 June 2009.
His double-cousin Princess Alix of Ligne had planned to travel with him, but took an earlier flight instead.
Pedro Luiz's body was among those retrieved from the ocean and was buried in Vassouras in the family's mausoleum on 5 July 2009.
Genealogy

Ancestry

Patrilineal descent

Pedro Luiz was a member of the House of Orléans-Braganza, a sub-branch of the House of Bourbon, itself a branch of the House of Capet and of the Robertians.
Pedro Luiz' patriline is the line from which he is descended father to son.



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
  AssignClass (8cd3f153-4fc6-4289-98b0-33f6cf5b1be8)
 Call ID: 8cd3f153-4fc6-4289-98b0-33f6cf5b1be8
  Args:
    source: Pedro_Luiz_of_Orléans-Braganza
    type: :Man
  AssignClass (18442308-be22-4dda-a889-c686e2c2ddf5)
 Call ID: 18442308-be22-4dda-a889-c686e2c2ddf5
  Args:
    type: :Person
    source: Pedro_Luiz_of_Orléans-Braganza
  AddLiteral (1e1b0fb8-cdb1-44ff-b7ef-95ec3bc33ec6)
 Call ID: 1e1b0fb8-cdb1-44ff-b7ef-95ec3bc33ec6
  Args:
    literal_value: 1983
    relation: :hasBirthYear
    source: Pedro_Luiz_of_Orléans-Braganza
    literal_type: xsd:integer
  AddLiteral (db5a0ad5-8a49-412c-86cb-2f5bac34a885)
 Call ID: db5a0ad5-8a49-412c-86cb-2f5bac34a885
  Args:
    literal_value: 2009
    relation: :hasDeathYear
    source: Pedro_Luiz_of_Orléans-Braganza
    literal_type: xsd:integer
  AssignClass (c1707529-9a4d-4a81-810d-757b6d605dcf)
 Call ID: c1707529-9a4d-4a81-810d-757b6d605dcf
  Args:
    type: :Man
    source: Pedro_Henrique_of_Orléans-Braganza
  AssignClass (e045d52a-d44f-477c-a791-689108ee88c6)
 Call ID: e045d52a-d44f-477c-a791-689108ee88c6
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    type: :Person
  AssignClass (09c07eb7-9eda-48e0-a517-71e9c99b7edc)
 Call ID: 09c07eb7-9eda-48e0-a517-71e9c99b7edc
  Args:
    type: :Woman
    source: Maria_Elisabeth_of_Bavaria
  AssignClass (2dcaefd9-4ab0-469e-bef1-44cb3db33089)
 Call ID: 2dcaefd9-4ab0-469e-bef1-44cb3db33089
  Args:
    type: :Person
    source: Maria_Elisabeth_of_Bavaria
  AssignClass (d02df5bc-0d58-444e-8d42-0a716bf471a6)
 Call ID: d02df5bc-0d58-444e-8d42-0a716bf471a6
  Args:
    source: António_of_Orléans-Braganza
    type: :Man
  AssignClass (7ddca164-8476-43e6-a3f3-1aca644aab91)
 Call ID: 7ddca164-8476-43e6-a3f3-1aca644aab91
  Args:
    source: António_of_Orléans-Braganza
    type: :Person
  AssignClass (ba32945d-78fe-4e18-a43f-c98748f151a4)
 Call ID: ba32945d-78fe-4e18-a43f-c98748f151a4
  Args:
    source: Christine_of_Ligne
    type: :Woman
  AssignClass (0285becc-23f9-4537-b787-4003d7a10b06)
 Call ID: 0285becc-23f9-4537-b787-4003d7a10b06
  Args:
    source: Christine_of_Ligne
    type: :Person
  AddTriple (a87a9508-8143-4ed8-b35b-e02750bd9749)
 Call ID: a87a9508-8143-4ed8-b35b-e02750bd9749
  Args:
    target: António_of_Orléans-Braganza
    relation: :hasFather
    source: Pedro_Luiz_of_Orléans-Braganza
  AddTriple (8993c0de-fe0d-445e-b11f-762e121bb29f)
 Call ID: 8993c0de-fe0d-445e-b11f-762e121bb29f
  Args:
    source: Pedro_Luiz_of_Orléans-Braganza
    target: Christine_of_Ligne
    relation: :hasMother
  AddTriple (cfbc6dbd-2d43-4dbe-9e2f-13d80ce84613)
 Call ID: cfbc6dbd-2d43-4dbe-9e2f-13d80ce84613
  Args:
    source: António_of_Orléans-Braganza
    relation: :hasFather
    target: Pedro_Henrique_of_Orléans-Braganza
  AddTriple (af042a5c-3b62-4c9f-b0e7-11ec710ff8bd)
 Call ID: af042a5c-3b62-4c9f-b0e7-11ec710ff8bd
  Args:
    source: António_of_Orléans-Braganza
    target: Maria_Elisabeth_of_Bavaria
    relation: :hasMother
  AssignClass (cd1316e8-faf4-4264-ab2e-5945837b0bb5)
 Call ID: cd1316e8-faf4-4264-ab2e-5945837b0bb5
  Args:
    source: Bertrand_of_Orléans-Braganza
    type: :Man
  AssignClass (c197d22d-d5d4-4798-92cf-ddd7db16a713)
 Call ID: c197d22d-d5d4-4798-92cf-ddd7db16a713
  Args:
    type: :Person
    source: Bertrand_of_Orléans-Braganza
  AddTriple (d33f4ae8-85e2-4efe-87d7-f1a3fb32ea62)
 Call ID: d33f4ae8-85e2-4efe-87d7-f1a3fb32ea62
  Args:
    source: Bertrand_of_Orléans-Braganza
    relation: :isBrotherOf
    target: António_of_Orléans-Braganza
  AssignClass (b3d8224e-c36a-482d-8dbc-bfb243e1201c)
 Call ID: b3d8224e-c36a-482d-8dbc-bfb243e1201c
  Args:
    source: Luiz_of_Orléans-Braganza
    type: :Man
  AssignClass (1dce56f4-c992-4b68-9034-89b67aee1327)
 Call ID: 1dce56f4-c992-4b68-9034-89b67aee1327
  Args:
    source: Luiz_of_Orléans-Braganza
    type: :Person
  AddTriple (e164477f-46f6-4fa1-b1d7-0f09754d6a64)
 Call ID: e164477f-46f6-4fa1-b1d7-0f09754d6a64
  Args:
    source: Luiz_of_Orléans-Braganza
    target: António_of_Orléans-Braganza
    relation: :isBrotherOf
  AssignClass (8645de50-9352-4f83-9cdb-cfc85a71f017)
 Call ID: 8645de50-9352-4f83-9cdb-cfc85a71f017
  Args:
    type: :Man
    source: Antoine_13th_Prince_of_Ligne
  AssignClass (08fa9def-3de9-4bc0-a448-ceaf41a64c87)
 Call ID: 08fa9def-3de9-4bc0-a448-ceaf41a64c87
  Args:
    type: :Person
    source: Antoine_13th_Prince_of_Ligne
  AssignClass (5e1d5cdf-36d9-4b2e-9ab0-a727d26ae773)
 Call ID: 5e1d5cdf-36d9-4b2e-9ab0-a727d26ae773
  Args:
    type: :Woman
    source: Alix_of_Luxembourg
  AssignClass (176d0bc6-d5f5-4548-b52c-71416daec58f)
 Call ID: 176d0bc6-d5f5-4548-b52c-71416daec58f
  Args:
    source: Alix_of_Luxembourg
    type: :Person
  AddTriple (bef1c024-a52d-467d-aa2d-8d4d80ae7acc)
 Call ID: bef1c024-a52d-467d-aa2d-8d4d80ae7acc
  Args:
    relation: :hasFather
    target: Antoine_13th_Prince_of_Ligne
    source: Christine_of_Ligne
  AddTriple (39cdc5e0-5e31-4a32-94eb-1ed5045eabda)
 Call ID: 39cdc5e0-5e31-4a32-94eb-1ed5045eabda
  Args:
    relation: :hasMother
    target: Alix_of_Luxembourg
    source: Christine_of_Ligne
  AssignClass (a5fb577d-a244-4f96-9764-ebf0c0544a68)
 Call ID: a5fb577d-a244-4f96-9764-ebf0c0544a68
  Args:
    source: Isabel_of_Brazil
    type: :Woman
  AssignClass (b9c3ef6f-6657-4dc7-b892-489ede8e352b)
 Call ID: b9c3ef6f-6657-4dc7-b892-489ede8e352b
  Args:
    source: Isabel_of_Brazil
    type: :Person
  AssignClass (63f88c6b-eaaa-4461-9b4a-c5445e79977f)
 Call ID: 63f88c6b-eaaa-4461-9b4a-c5445e79977f
  Args:
    source: Gaston_of_Orléans_Count_of_Eu
    type: :Man
  AssignClass (900695c5-659b-43e2-9979-ab1ef4c4a790)
 Call ID: 900695c5-659b-43e2-9979-ab1ef4c4a790
  Args:
    source: Gaston_of_Orléans_Count_of_Eu
    type: :Person
  AssignClass (761b2975-1aa1-4a92-8b00-bc6630533a84)
 Call ID: 761b2975-1aa1-4a92-8b00-bc6630533a84
  Args:
    type: :Man
    source: Pedro_II_of_Brazil
  AssignClass (9c614452-70ae-46cc-93fe-86c0a4d28d19)
 Call ID: 9c614452-70ae-46cc-93fe-86c0a4d28d19
  Args:
    type: :Person
    source: Pedro_II_of_Brazil
  AssignClass (9decf2b9-b03c-46f4-99a7-2a31d7c199df)
 Call ID: 9decf2b9-b03c-46f4-99a7-2a31d7c199df
  Args:
    type: :Woman
    source: Teresa_Cristina_of_Brazil
  AssignClass (2bf617d1-8f3f-4c2d-967f-0dd4f0934231)
 Call ID: 2bf617d1-8f3f-4c2d-967f-0dd4f0934231
  Args:
    type: :Person
    source: Teresa_Cristina_of_Brazil
  Finish (822e9f62-c273-4e42-af25-5cf61ab93fa4)
 Call ID: 822e9f62-c273-4e42-af25-5cf61ab93fa4
  Args: