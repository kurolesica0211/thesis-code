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
Princess Nathalie of Sayn-Wittgenstein-Berleburg (Nathalie Xenia Margrethe Benedikte; born 2 May 1975) is a Danish equestrian, an Olympian, and the daughter of Princess Benedikte of Denmark and Prince Richard of Sayn-Wittgenstein-Berleburg.
She is the niece of Queen Margrethe II of Denmark and King Constantine II of Greece.
Her first cousin is King Frederik X of Denmark.
Early life

Princess Nathalie was born on 2 May 1975 in Copenhagen, Denmark, the youngest of three children of Princess Benedikte of Denmark and Prince Richard of Sayn-Wittgenstein-Berleburg.
She grew up at Schloss Berleburg in Bad Berleburg, Germany.
Nathalie and her sister Alexandra became Danish citizens on 19 May 1998.
Neither she nor her siblings are in line of succession to the Danish throne, as that would have required taking up permanent residence in Denmark when reaching the age of mandatory education.
Equestrian career

In 1994, Princess Nathalie began training at the Swedish stud Flyinge with Kyra Kyrklund, a former world champion in dressage.
Nathalie was selected as a reserve rider for the 2000 Olympic team.
She finished 12th in the individual event and helped Denmark to a 4th-place team finish.
In January 2017, Nathalie was named head coach of the Danish national dressage team.
In autumn 2005, she opened her own stud farm, which is based in Bad Berleburg.
Marriage and children

On 4 January 2010, Princess Nathalie's engagement to German horse breeder Alexander Johannsmann (born 6 December 1977), son of showjumper Heinrich-Wilhelm Johannsmann, was announced.
The couple married civilly 27 May 2010 and religiously the following year, on 18 June 2011 at the Protestant Stadtkirche in Berleburg, Germany.
Princess Nathalie gave birth to a son, Konstantin Gustav Heinrich Richard, on 24 July 2010.
Konstantin's godparents were Crown Princess Mary of Denmark, his aunt Ann-Kathrin Johannsmann, and his uncle Prince Gustav.
On 28 January 2015, she gave birth to her second child, a daughter named Louisa Margareta Benedikte Hanna, in Bad Berleburg, Germany.
On 15 August 2022, the Danish court confirmed that Nathalie and Johannsmann had divorced.



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
  AssignClass (55606fab-353b-45e8-86b1-4f636e63dfeb)
 Call ID: 55606fab-353b-45e8-86b1-4f636e63dfeb
  Args:
    type: :Woman
    source: PrincessNathalie
  AssignClass (8b30d481-477d-4b4e-86b9-f0757c21d704)
 Call ID: 8b30d481-477d-4b4e-86b9-f0757c21d704
  Args:
    source: PrincessNathalie
    type: :Person
  AddLiteral (3a5cfb88-35d4-466a-87c5-80c51d951995)
 Call ID: 3a5cfb88-35d4-466a-87c5-80c51d951995
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1975
    source: PrincessNathalie
  AssignClass (763ae920-05cd-4dab-a458-5c99f5c4058e)
 Call ID: 763ae920-05cd-4dab-a458-5c99f5c4058e
  Args:
    source: PrincessBenedikte
    type: :Woman
  AssignClass (d51c1283-6a2d-4eb5-a9df-0352ad892697)
 Call ID: d51c1283-6a2d-4eb5-a9df-0352ad892697
  Args:
    type: :Person
    source: PrincessBenedikte
  AssignClass (216f237e-3046-4133-8dfb-e65e757c524f)
 Call ID: 216f237e-3046-4133-8dfb-e65e757c524f
  Args:
    source: PrinceRichard
    type: :Man
  AssignClass (52cdbc05-e5bd-4395-869f-3188dc7afc91)
 Call ID: 52cdbc05-e5bd-4395-869f-3188dc7afc91
  Args:
    type: :Person
    source: PrinceRichard
  AddTriple (80f6cf06-d118-46fe-ae05-daad05338c91)
 Call ID: 80f6cf06-d118-46fe-ae05-daad05338c91
  Args:
    target: PrincessBenedikte
    source: PrincessNathalie
    relation: :hasMother
  AddTriple (9c50b21c-4976-48b3-82ad-2475d0f57cd8)
 Call ID: 9c50b21c-4976-48b3-82ad-2475d0f57cd8
  Args:
    source: PrincessNathalie
    target: PrinceRichard
    relation: :hasFather
  AssignClass (34cdfd2c-e5cb-421a-8177-c52329a3f883)
 Call ID: 34cdfd2c-e5cb-421a-8177-c52329a3f883
  Args:
    source: QueenMargretheII
    type: :Woman
  AssignClass (d33c298a-017e-4b9c-8742-29ae4e88661a)
 Call ID: d33c298a-017e-4b9c-8742-29ae4e88661a
  Args:
    source: QueenMargretheII
    type: :Person
  AssignClass (ec98de92-02f3-44da-954c-f857f1fccc90)
 Call ID: ec98de92-02f3-44da-954c-f857f1fccc90
  Args:
    type: :Man
    source: KingConstantineII
  AssignClass (9f8b0a9d-b21c-454d-9f3a-8dd8633e18fd)
 Call ID: 9f8b0a9d-b21c-454d-9f3a-8dd8633e18fd
  Args:
    type: :Person
    source: KingConstantineII
  AssignClass (99b03f31-f797-47f7-85a2-25ae0dfabd44)
 Call ID: 99b03f31-f797-47f7-85a2-25ae0dfabd44
  Args:
    source: KingFrederikX
    type: :Man
  AssignClass (ba05a70d-046c-4d6b-bd5a-e798759e3bf3)
 Call ID: ba05a70d-046c-4d6b-bd5a-e798759e3bf3
  Args:
    source: KingFrederikX
    type: :Person
  AssignClass (45f1db10-76f9-4198-920b-a57888a9c1ce)
 Call ID: 45f1db10-76f9-4198-920b-a57888a9c1ce
  Args:
    type: :Woman
    source: Alexandra
  AssignClass (f1df2056-36f0-441a-bddc-48d116c66051)
 Call ID: f1df2056-36f0-441a-bddc-48d116c66051
  Args:
    source: Alexandra
    type: :Person
  AddTriple (028ae5d0-b20a-462a-9c00-68ded2df39ae)
 Call ID: 028ae5d0-b20a-462a-9c00-68ded2df39ae
  Args:
    relation: :hasSister
    target: Alexandra
    source: PrincessNathalie
  AssignClass (48bb6180-67b0-416a-b986-ad7f13b4df69)
 Call ID: 48bb6180-67b0-416a-b986-ad7f13b4df69
  Args:
    source: AlexanderJohannsmann
    type: :Man
  AssignClass (425cfb73-9b85-449f-96f8-76c8b07cec18)
 Call ID: 425cfb73-9b85-449f-96f8-76c8b07cec18
  Args:
    source: AlexanderJohannsmann
    type: :Person
  AddLiteral (915a8497-b5a6-468a-84a2-6964bb8446d1)
 Call ID: 915a8497-b5a6-468a-84a2-6964bb8446d1
  Args:
    literal_value: 1977
    source: AlexanderJohannsmann
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (c7137171-6a1c-4543-bcfe-da9909799cb0)
 Call ID: c7137171-6a1c-4543-bcfe-da9909799cb0
  Args:
    source: Heinrich-WilhelmJohannsmann
    type: :Man
  AssignClass (f4b0586b-b91d-4277-94e7-bf3e5caf6d0d)
 Call ID: f4b0586b-b91d-4277-94e7-bf3e5caf6d0d
  Args:
    source: Heinrich-WilhelmJohannsmann
    type: :Person
  AddTriple (35bf0740-2a6a-4c87-ad3c-d064ca09c364)
 Call ID: 35bf0740-2a6a-4c87-ad3c-d064ca09c364
  Args:
    source: AlexanderJohannsmann
    target: Heinrich-WilhelmJohannsmann
    relation: :hasFather
  AddLiteral (f3b195ec-ee3a-4f7f-9cee-b7baad2b553e)
 Call ID: f3b195ec-ee3a-4f7f-9cee-b7baad2b553e
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 2010
    source: PrincessNathalie
  AssignClass (4df583ca-9ee9-4f8e-a05c-29e31d330848)
 Call ID: 4df583ca-9ee9-4f8e-a05c-29e31d330848
  Args:
    type: :Man
    source: KonstantinGustavHeinrichRichard
  AssignClass (c4907e71-fdda-49be-a3cd-48a6d1c9cdfb)
 Call ID: c4907e71-fdda-49be-a3cd-48a6d1c9cdfb
  Args:
    source: KonstantinGustavHeinrichRichard
    type: :Person
  AddTriple (cba18718-7528-4293-9781-709e41fd1a28)
 Call ID: cba18718-7528-4293-9781-709e41fd1a28
  Args:
    relation: :hasMother
    target: PrincessNathalie
    source: KonstantinGustavHeinrichRichard
  AddTriple (7625fa27-88ee-4729-8857-af0dbbe232ce)
 Call ID: 7625fa27-88ee-4729-8857-af0dbbe232ce
  Args:
    relation: :hasFather
    target: AlexanderJohannsmann
    source: KonstantinGustavHeinrichRichard
  AssignClass (13000c2f-a66d-4ee5-8b25-d0c2f2136c32)
 Call ID: 13000c2f-a66d-4ee5-8b25-d0c2f2136c32
  Args:
    source: LouisaMargaretaBenedikteHanna
    type: :Woman
  AssignClass (99f412e0-763c-4e01-adf6-516dceeeb689)
 Call ID: 99f412e0-763c-4e01-adf6-516dceeeb689
  Args:
    source: LouisaMargaretaBenedikteHanna
    type: :Person
  AddTriple (932f32ef-27b9-4be6-a6bf-fb7a85d09edd)
 Call ID: 932f32ef-27b9-4be6-a6bf-fb7a85d09edd
  Args:
    relation: :hasMother
    target: PrincessNathalie
    source: LouisaMargaretaBenedikteHanna
  AddTriple (68d4abb7-18e6-4665-84a5-367776ccd871)
 Call ID: 68d4abb7-18e6-4665-84a5-367776ccd871
  Args:
    target: AlexanderJohannsmann
    source: LouisaMargaretaBenedikteHanna
    relation: :hasFather
  AssignClass (ababd618-11ce-40a2-916d-48fcf389564f)
 Call ID: ababd618-11ce-40a2-916d-48fcf389564f
  Args:
    type: :Woman
    source: Ann-KathrinJohannsmann
  AssignClass (ffebe631-2924-4d8b-8762-029bc1aa5ef9)
 Call ID: ffebe631-2924-4d8b-8762-029bc1aa5ef9
  Args:
    type: :Person
    source: Ann-KathrinJohannsmann
  AssignClass (9c4fe32c-319c-4755-9a46-c31451d8c8a7)
 Call ID: 9c4fe32c-319c-4755-9a46-c31451d8c8a7
  Args:
    source: PrinceGustav
    type: :Man
  AssignClass (74f367c5-1ffa-4156-bf10-2729424c7c33)
 Call ID: 74f367c5-1ffa-4156-bf10-2729424c7c33
  Args:
    source: PrinceGustav
    type: :Person
  Finish (b18974af-5cb3-4299-8a48-3080e618eac3)
 Call ID: b18974af-5cb3-4299-8a48-3080e618eac3
  Args: