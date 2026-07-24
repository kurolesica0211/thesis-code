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
  AssignClass (15775c5c-a8b7-40b5-a07c-02e78f5cccae)
 Call ID: 15775c5c-a8b7-40b5-a07c-02e78f5cccae
  Args:
    type: :Man
    source: Pedro_Luiz_of_Orléans-Braganza
  AssignClass (87da8bc9-5683-41e2-b0b2-b54f2dcf31fe)
 Call ID: 87da8bc9-5683-41e2-b0b2-b54f2dcf31fe
  Args:
    type: :Person
    source: Pedro_Luiz_of_Orléans-Braganza
  AddLiteral (00aa84b4-bcba-4481-9af2-70412590677a)
 Call ID: 00aa84b4-bcba-4481-9af2-70412590677a
  Args:
    literal_value: 1983
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Pedro_Luiz_of_Orléans-Braganza
  AddLiteral (88c5161c-1378-4d2a-b66b-0f961b42683f)
 Call ID: 88c5161c-1378-4d2a-b66b-0f961b42683f
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2009
    source: Pedro_Luiz_of_Orléans-Braganza
  AssignClass (ec33c756-7090-4da4-9313-e80f9d5243bc)
 Call ID: ec33c756-7090-4da4-9313-e80f9d5243bc
  Args:
    type: :Man
    source: Pedro_Henrique_of_Orléans-Braganza
  AssignClass (08aabd17-2fea-43f0-be6e-c401e7b6a0b2)
 Call ID: 08aabd17-2fea-43f0-be6e-c401e7b6a0b2
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    type: :Person
  AssignClass (e5d31709-c940-4f9c-bc8d-8025f0b20ad5)
 Call ID: e5d31709-c940-4f9c-bc8d-8025f0b20ad5
  Args:
    source: Maria_Elisabeth_of_Bavaria
    type: :Woman
  AssignClass (8e3706a2-60a5-4835-bb5e-494be2fd6ec9)
 Call ID: 8e3706a2-60a5-4835-bb5e-494be2fd6ec9
  Args:
    source: Maria_Elisabeth_of_Bavaria
    type: :Person
  AddTriple (0bf5f4a3-0dc2-424f-8dd1-b13c5287cfeb)
 Call ID: 0bf5f4a3-0dc2-424f-8dd1-b13c5287cfeb
  Args:
    source: Pedro_Luiz_of_Orléans-Braganza
    target: António_of_Orléans-Braganza
    relation: :hasFather
  AddTriple (46c50e98-b3a0-4309-8003-fce4aac9d8cb)
 Call ID: 46c50e98-b3a0-4309-8003-fce4aac9d8cb
  Args:
    relation: :hasMother
    target: Christine_of_Ligne
    source: Pedro_Luiz_of_Orléans-Braganza
  AssignClass (07ad9060-b933-430e-b11e-f44d36158629)
 Call ID: 07ad9060-b933-430e-b11e-f44d36158629
  Args:
    source: António_of_Orléans-Braganza
    type: :Man
  AssignClass (bd446a90-6fbf-4ce6-b820-fcf94c5176ed)
 Call ID: bd446a90-6fbf-4ce6-b820-fcf94c5176ed
  Args:
    source: António_of_Orléans-Braganza
    type: :Person
  AssignClass (c6989c87-a843-47b4-96d5-3401c88ae71d)
 Call ID: c6989c87-a843-47b4-96d5-3401c88ae71d
  Args:
    source: Christine_of_Ligne
    type: :Woman
  AssignClass (ff2adf2a-4652-4816-a12d-c2f12697d703)
 Call ID: ff2adf2a-4652-4816-a12d-c2f12697d703
  Args:
    type: :Person
    source: Christine_of_Ligne
  AddTriple (555b1fa4-7277-4e37-992f-d6fd0c951e9d)
 Call ID: 555b1fa4-7277-4e37-992f-d6fd0c951e9d
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    target: António_of_Orléans-Braganza
    relation: :isFatherOf
  AddTriple (0cefe5c7-8700-43f7-b866-a0980dd3db34)
 Call ID: 0cefe5c7-8700-43f7-b866-a0980dd3db34
  Args:
    relation: :isMotherOf
    target: António_of_Orléans-Braganza
    source: Maria_Elisabeth_of_Bavaria
  AddTriple (22de620e-f7df-4a02-8744-71d4549892bb)
 Call ID: 22de620e-f7df-4a02-8744-71d4549892bb
  Args:
    relation: :isFatherOf
    source: Antoine_13th_Prince_of_Ligne
    target: Christine_of_Ligne
  AddTriple (d3a89199-5be7-46b0-b5e8-9badd325f98d)
 Call ID: d3a89199-5be7-46b0-b5e8-9badd325f98d
  Args:
    target: Christine_of_Ligne
    source: Alix_of_Luxembourg
    relation: :isMotherOf
  AssignClass (fa42d9d3-0ce0-4d79-b5f2-a81ce62769de)
 Call ID: fa42d9d3-0ce0-4d79-b5f2-a81ce62769de
  Args:
    type: :Man
    source: Antoine_13th_Prince_of_Ligne
  AssignClass (c664b0e5-b526-4870-978f-642a08ecc25c)
 Call ID: c664b0e5-b526-4870-978f-642a08ecc25c
  Args:
    source: Antoine_13th_Prince_of_Ligne
    type: :Person
  AssignClass (865caa09-beb6-41b8-9c25-70e65a014f85)
 Call ID: 865caa09-beb6-41b8-9c25-70e65a014f85
  Args:
    source: Alix_of_Luxembourg
    type: :Woman
  AssignClass (db4f2249-d7ba-4102-a870-5b20b537340c)
 Call ID: db4f2249-d7ba-4102-a870-5b20b537340c
  Args:
    type: :Person
    source: Alix_of_Luxembourg
  AssignClass (deeb6bc6-7418-4f97-8dfe-3f9aed56e1a8)
 Call ID: deeb6bc6-7418-4f97-8dfe-3f9aed56e1a8
  Args:
    source: Luiz_of_Orléans-Braganza
    type: :Man
  AssignClass (083557b3-196f-4b1d-ad4d-9f8cca4a9273)
 Call ID: 083557b3-196f-4b1d-ad4d-9f8cca4a9273
  Args:
    source: Luiz_of_Orléans-Braganza
    type: :Person
  AssignClass (a653b640-cc38-4228-a380-4915b8ea8a59)
 Call ID: a653b640-cc38-4228-a380-4915b8ea8a59
  Args:
    type: :Man
    source: Bertrand_of_Orléans-Braganza
  AssignClass (3b1d8195-5301-467d-9839-d68d7cd65ee7)
 Call ID: 3b1d8195-5301-467d-9839-d68d7cd65ee7
  Args:
    type: :Person
    source: Bertrand_of_Orléans-Braganza
  AddTriple (08436373-4da8-45b4-bf9c-11e7f741366f)
 Call ID: 08436373-4da8-45b4-bf9c-11e7f741366f
  Args:
    relation: :isBrotherOf
    source: Luiz_of_Orléans-Braganza
    target: António_of_Orléans-Braganza
  AddTriple (1cccb006-f2c8-4940-b733-ff02c95c82af)
 Call ID: 1cccb006-f2c8-4940-b733-ff02c95c82af
  Args:
    relation: :isBrotherOf
    source: Bertrand_of_Orléans-Braganza
    target: António_of_Orléans-Braganza
  Finish (bdcf0781-fa4e-4b4b-baae-dbd5cdcdb69b)
 Call ID: bdcf0781-fa4e-4b4b-baae-dbd5cdcdb69b
  Args: