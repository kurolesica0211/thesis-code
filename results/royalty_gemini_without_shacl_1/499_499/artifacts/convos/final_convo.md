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
  AssignClass (21e15071-fbcd-4926-9695-d893b639f914)
 Call ID: 21e15071-fbcd-4926-9695-d893b639f914
  Args:
    type: :Man
    source: Pedro_Luiz_of_Orleans-Braganza
  AssignClass (e7016b0e-9b78-46f7-bdbe-5f16cd8107a3)
 Call ID: e7016b0e-9b78-46f7-bdbe-5f16cd8107a3
  Args:
    source: Pedro_Luiz_of_Orleans-Braganza
    type: :Person
  AddLiteral (33a71039-c6eb-484f-902e-41b0bde51d63)
 Call ID: 33a71039-c6eb-484f-902e-41b0bde51d63
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Pedro_Luiz_of_Orleans-Braganza
    literal_value: 1983
  AddLiteral (9b89d5ad-b296-494f-90de-c71e7214b3c9)
 Call ID: 9b89d5ad-b296-494f-90de-c71e7214b3c9
  Args:
    literal_value: 2009
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Pedro_Luiz_of_Orleans-Braganza
  AssignClass (7a31d538-6444-4aa5-af24-62a7f9dbed26)
 Call ID: 7a31d538-6444-4aa5-af24-62a7f9dbed26
  Args:
    source: Prince_Pedro_Henrique_of_Orleans-Braganza
    type: :Man
  AssignClass (676a441b-25a4-471f-8b7e-0c160858a083)
 Call ID: 676a441b-25a4-471f-8b7e-0c160858a083
  Args:
    source: Prince_Pedro_Henrique_of_Orleans-Braganza
    type: :Person
  AssignClass (3afaec92-1618-4d0c-94cc-f6a68dc4d06a)
 Call ID: 3afaec92-1618-4d0c-94cc-f6a68dc4d06a
  Args:
    source: Princess_Maria_Elisabeth_of_Bavaria
    type: :Woman
  AssignClass (c9aa3739-7ab1-4563-b387-a6663e6ca4b6)
 Call ID: c9aa3739-7ab1-4563-b387-a6663e6ca4b6
  Args:
    type: :Person
    source: Princess_Maria_Elisabeth_of_Bavaria
  AssignClass (1a2551d8-2fcf-45d0-a1f5-6205f434b4b1)
 Call ID: 1a2551d8-2fcf-45d0-a1f5-6205f434b4b1
  Args:
    type: :Man
    source: Prince_Antonio_of_Orleans-Braganza
  AssignClass (104e86d5-52f4-4f00-a602-77afb1c44cee)
 Call ID: 104e86d5-52f4-4f00-a602-77afb1c44cee
  Args:
    source: Prince_Antonio_of_Orleans-Braganza
    type: :Person
  AssignClass (3c2ceae3-a9c0-4e7c-895e-2d586820b29c)
 Call ID: 3c2ceae3-a9c0-4e7c-895e-2d586820b29c
  Args:
    source: Princess_Christine_of_Ligne
    type: :Woman
  AssignClass (ce1f8400-f562-460e-bbba-3fb1111bcae6)
 Call ID: ce1f8400-f562-460e-bbba-3fb1111bcae6
  Args:
    type: :Person
    source: Princess_Christine_of_Ligne
  AssignClass (784e9081-4f2d-4033-9336-53c4d381ceb8)
 Call ID: 784e9081-4f2d-4033-9336-53c4d381ceb8
  Args:
    type: :Man
    source: Bertrand_of_Orleans-Braganza
  AssignClass (001a6934-c2db-4410-98ee-a48413e3957b)
 Call ID: 001a6934-c2db-4410-98ee-a48413e3957b
  Args:
    type: :Person
    source: Bertrand_of_Orleans-Braganza
  AssignClass (447c97cf-5efd-4125-b0cd-b649f54986d7)
 Call ID: 447c97cf-5efd-4125-b0cd-b649f54986d7
  Args:
    type: :Man
    source: Prince_Luiz_of_Orleans-Braganza
  AssignClass (af982e88-5329-4495-844a-c359078cd6a0)
 Call ID: af982e88-5329-4495-844a-c359078cd6a0
  Args:
    source: Prince_Luiz_of_Orleans-Braganza
    type: :Person
  AddTriple (57a13119-6001-403d-a440-f56efed23772)
 Call ID: 57a13119-6001-403d-a440-f56efed23772
  Args:
    target: Prince_Antonio_of_Orleans-Braganza
    relation: :hasFather
    source: Pedro_Luiz_of_Orleans-Braganza
  AddTriple (33f92bc6-7d94-43c5-9cd1-2d9f0ec77798)
 Call ID: 33f92bc6-7d94-43c5-9cd1-2d9f0ec77798
  Args:
    source: Pedro_Luiz_of_Orleans-Braganza
    target: Princess_Christine_of_Ligne
    relation: :hasMother
  AddTriple (f32c32f0-efea-45ba-ad9a-2b9477740bec)
 Call ID: f32c32f0-efea-45ba-ad9a-2b9477740bec
  Args:
    relation: :hasFather
    target: Prince_Pedro_Henrique_of_Orleans-Braganza
    source: Prince_Antonio_of_Orleans-Braganza
  AddTriple (2307ad5f-c4a6-44c1-99bd-431b823829dd)
 Call ID: 2307ad5f-c4a6-44c1-99bd-431b823829dd
  Args:
    source: Prince_Antonio_of_Orleans-Braganza
    relation: :hasMother
    target: Princess_Maria_Elisabeth_of_Bavaria
  AddTriple (f4090c21-6d9c-42f5-910a-28203a0ce163)
 Call ID: f4090c21-6d9c-42f5-910a-28203a0ce163
  Args:
    source: Prince_Antonio_of_Orleans-Braganza
    target: Bertrand_of_Orleans-Braganza
    relation: :isBrotherOf
  AddTriple (6104eaf3-9537-4057-b89f-227e1fd4cc15)
 Call ID: 6104eaf3-9537-4057-b89f-227e1fd4cc15
  Args:
    source: Prince_Antonio_of_Orleans-Braganza
    relation: :isBrotherOf
    target: Prince_Luiz_of_Orleans-Braganza
  AddTriple (c6bcdaf5-2c47-4104-91bb-dea5ba232fc7)
 Call ID: c6bcdaf5-2c47-4104-91bb-dea5ba232fc7
  Args:
    source: Bertrand_of_Orleans-Braganza
    target: Prince_Luiz_of_Orleans-Braganza
    relation: :isBrotherOf
  Finish (46b5d385-7ed8-4959-920e-c0c637c02dc0)
 Call ID: 46b5d385-7ed8-4959-920e-c0c637c02dc0
  Args: