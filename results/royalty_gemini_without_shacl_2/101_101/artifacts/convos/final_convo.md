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
Gustav, 7th Prince of Sayn-Wittgenstein-Berleburg (Gustav Frederik Philip Richard; born 12 January 1969), is the eldest child and only son of Princess Benedikte of Denmark and Richard, 6th Prince of Sayn-Wittgenstein-Berleburg.
His first cousin is King Frederik X of Denmark.
Biography

Prince Gustav is the head of the House of Sayn-Wittgenstein-Berleburg, the senior branch of the formerly princely house of Sayn-Wittgenstein.
He resides at Schloss Berleburg-Wittgenstein in the town of Bad Berleburg, in North Rhine-Westphalia, Germany.
He is the son of Prince Richard of Sayn-Wittgenstein-Berleburg and Princess Benedikte of Denmark and has two sisters, Princess Alexandra of Sayn-Wittgenstein-Berleburg and Princess Nathalie of Sayn-Wittgenstein-Berleburg.
The principality and princely title of Sayn-Wittgenstein-Berleburg descended, historically, according to semi-Salic primogeniture.
If Gustav were to die without legitimate issue, the family heritage would devolve upon his father's younger brother, Prince Robin zu Sayn-Wittgenstein-Berleburg.
Gustav was formerly engaged to be married to Elvire Pasté de Rochefort (granddaughter of French Ambassador André Rodocanachi and wife Nada Diplarakou, herself sister of Aliki Diplarakou and grand-aunt of Princess Sibilla of Luxembourg); the engagement was announced on 16 August 2000 and the wedding planned for 12 May 2001 in Paris.
For many years, he resided with his partner, Carina Axelsson, although they were unable to marry due to a clause in Gustav's grandfather's will preventing him from inheriting family property if he marries someone not of Protestant, noble and Aryan descent.
However, on 27 April 2022, the Danish court confirmed that Gustav could marry Axelsson on 3 June 2022, civilly and on 4 June 2022, religiously in Bad Berleburg.
The couple's son, Prince Gustav Albrecht, was born on 26 May 2023 in the United States via surrogacy.
On 26 April 2024, the couple welcomed their second child, a girl, Princess Mafalda, also via surrogacy.
He is the godfather of Count Richard von Pfeil und Klein-Ellguth, son of his sister Alexandra; Konstantin Johannsmann, son of his second sister Nathalie; and Prince Vincent of Denmark, son of his first cousin, Frederik X.


Ancestry




References

External links



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
  AssignClass (b0c4e7da-b7f9-42c8-9d13-483eefccc796)
 Call ID: b0c4e7da-b7f9-42c8-9d13-483eefccc796
  Args:
    source: Gustav
    type: :Man
  AssignClass (dbba01de-9997-42e5-8cf8-9575c57d9908)
 Call ID: dbba01de-9997-42e5-8cf8-9575c57d9908
  Args:
    source: Gustav
    type: :Person
  AddLiteral (913747e7-657c-406d-bc69-30c3bf05ef0f)
 Call ID: 913747e7-657c-406d-bc69-30c3bf05ef0f
  Args:
    literal_type: xsd:integer
    literal_value: 1969
    relation: :hasBirthYear
    source: Gustav
  AssignClass (737da7d7-c071-46f4-b5cb-0c1bf447ff43)
 Call ID: 737da7d7-c071-46f4-b5cb-0c1bf447ff43
  Args:
    type: :Woman
    source: Princess_Benedikte_of_Denmark
  AssignClass (4c737668-71d3-4a4b-8284-29f9355e7639)
 Call ID: 4c737668-71d3-4a4b-8284-29f9355e7639
  Args:
    type: :Person
    source: Princess_Benedikte_of_Denmark
  AssignClass (e13109c9-33cc-46a2-8810-f09762bc9f14)
 Call ID: e13109c9-33cc-46a2-8810-f09762bc9f14
  Args:
    source: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
    type: :Man
  AssignClass (8ea9ef28-937a-41a5-9bb5-ece615281bd6)
 Call ID: 8ea9ef28-937a-41a5-9bb5-ece615281bd6
  Args:
    source: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AddTriple (439221ad-31ec-4edc-b1dd-21b46aeb39cb)
 Call ID: 439221ad-31ec-4edc-b1dd-21b46aeb39cb
  Args:
    target: Princess_Benedikte_of_Denmark
    relation: :hasMother
    source: Gustav
  AddTriple (fa4ab293-047a-4d98-b0bd-b69d324801e2)
 Call ID: fa4ab293-047a-4d98-b0bd-b69d324801e2
  Args:
    relation: :hasFather
    source: Gustav
    target: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
  AssignClass (cfb7b60f-b0aa-48be-8040-b98be75059e0)
 Call ID: cfb7b60f-b0aa-48be-8040-b98be75059e0
  Args:
    type: :Woman
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (5df91932-2d5c-4db3-bb15-a84593013da5)
 Call ID: 5df91932-2d5c-4db3-bb15-a84593013da5
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AssignClass (e0086631-74b7-47a1-a072-8fc6a97f1978)
 Call ID: e0086631-74b7-47a1-a072-8fc6a97f1978
  Args:
    type: :Woman
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
  AssignClass (2ae365f9-34af-438e-b9f6-561d617a6a05)
 Call ID: 2ae365f9-34af-438e-b9f6-561d617a6a05
  Args:
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AddTriple (fe76db3f-f205-48f8-bd97-a52d83fb99b1)
 Call ID: fe76db3f-f205-48f8-bd97-a52d83fb99b1
  Args:
    relation: :isSiblingOf
    source: Gustav
    target: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AddTriple (10467381-f6fb-427c-8369-795022718fe6)
 Call ID: 10467381-f6fb-427c-8369-795022718fe6
  Args:
    source: Gustav
    relation: :isSiblingOf
    target: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
  AssignClass (feed890b-012d-4298-a6f3-9ac0ce30f394)
 Call ID: feed890b-012d-4298-a6f3-9ac0ce30f394
  Args:
    type: :Man
    source: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
  AssignClass (efaa6455-26a7-4b61-b6bc-a49e9ae6789b)
 Call ID: efaa6455-26a7-4b61-b6bc-a49e9ae6789b
  Args:
    source: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
    type: :Person
  AddTriple (fe0a9c79-73b0-4b2f-8cf3-7cdad9e732e8)
 Call ID: fe0a9c79-73b0-4b2f-8cf3-7cdad9e732e8
  Args:
    relation: :isBrotherOf
    source: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
    target: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
  AssignClass (8cd9920d-2961-4643-9e8f-e7219c991221)
 Call ID: 8cd9920d-2961-4643-9e8f-e7219c991221
  Args:
    source: Carina_Axelsson
    type: :Woman
  AssignClass (86e55e1e-c711-48ae-a886-138741b2ea43)
 Call ID: 86e55e1e-c711-48ae-a886-138741b2ea43
  Args:
    source: Carina_Axelsson
    type: :Person
  AssignClass (50ea315e-b890-4b71-9db5-58c016ae873b)
 Call ID: 50ea315e-b890-4b71-9db5-58c016ae873b
  Args:
    source: Prince_Gustav_Albrecht
    type: :Man
  AssignClass (6198e1d7-ed5c-48d5-8048-8b6cc31b3fec)
 Call ID: 6198e1d7-ed5c-48d5-8048-8b6cc31b3fec
  Args:
    source: Prince_Gustav_Albrecht
    type: :Person
  AddTriple (1a250457-dbdb-43af-adb4-6fe9047ec36c)
 Call ID: 1a250457-dbdb-43af-adb4-6fe9047ec36c
  Args:
    source: Prince_Gustav_Albrecht
    relation: :isSonOf
    target: Gustav
  AddTriple (8d5e38e4-a355-4671-8a6e-e44308607e4f)
 Call ID: 8d5e38e4-a355-4671-8a6e-e44308607e4f
  Args:
    source: Prince_Gustav_Albrecht
    relation: :isSonOf
    target: Carina_Axelsson
  AssignClass (2c928a6e-eadb-42d4-a234-522bd8cfc905)
 Call ID: 2c928a6e-eadb-42d4-a234-522bd8cfc905
  Args:
    source: Princess_Mafalda
    type: :Woman
  AssignClass (ccff8a7a-4d35-44c2-97fc-fe1d815828cc)
 Call ID: ccff8a7a-4d35-44c2-97fc-fe1d815828cc
  Args:
    type: :Person
    source: Princess_Mafalda
  AddTriple (43c00950-b2d8-4061-9635-fc510b385c8f)
 Call ID: 43c00950-b2d8-4061-9635-fc510b385c8f
  Args:
    relation: :isDaughterOf
    source: Princess_Mafalda
    target: Gustav
  AddTriple (fa2dc9a7-a8cf-4671-b6e2-afeda3aacf1b)
 Call ID: fa2dc9a7-a8cf-4671-b6e2-afeda3aacf1b
  Args:
    source: Princess_Mafalda
    relation: :isDaughterOf
    target: Carina_Axelsson
  Finish (96af5d95-da5a-48d8-beee-b9ed2e1a3508)
 Call ID: 96af5d95-da5a-48d8-beee-b9ed2e1a3508
  Args: