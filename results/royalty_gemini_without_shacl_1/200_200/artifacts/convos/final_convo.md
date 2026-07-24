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
  AssignClass (6bf8838c-0356-4f04-aa52-499b9782a2f2)
 Call ID: 6bf8838c-0356-4f04-aa52-499b9782a2f2
  Args:
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    type: :Woman
  AssignClass (29b8a6d5-e6aa-40ef-8117-ce47fe3c6c8c)
 Call ID: 29b8a6d5-e6aa-40ef-8117-ce47fe3c6c8c
  Args:
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AddLiteral (c24674ba-a73c-44fb-b5c4-0d083c4155be)
 Call ID: c24674ba-a73c-44fb-b5c4-0d083c4155be
  Args:
    relation: :hasBirthYear
    literal_value: 1975
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    literal_type: xsd:integer
  AssignClass (42938ed5-eba8-466f-87ee-8b24d6456461)
 Call ID: 42938ed5-eba8-466f-87ee-8b24d6456461
  Args:
    type: :Woman
    source: Princess_Benedikte_of_Denmark
  AssignClass (ed14f361-7011-46ea-a9e1-7135129559e0)
 Call ID: ed14f361-7011-46ea-a9e1-7135129559e0
  Args:
    type: :Person
    source: Princess_Benedikte_of_Denmark
  AssignClass (d5d7e42f-aa12-4754-acbe-1b004d645eae)
 Call ID: d5d7e42f-aa12-4754-acbe-1b004d645eae
  Args:
    type: :Man
    source: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
  AssignClass (7968e327-f6af-4c3c-89a2-646d55138c2a)
 Call ID: 7968e327-f6af-4c3c-89a2-646d55138c2a
  Args:
    source: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AddTriple (9ddb3969-989c-4916-ac21-15720cae4d38)
 Call ID: 9ddb3969-989c-4916-ac21-15720cae4d38
  Args:
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    relation: :isChildOf
    target: Princess_Benedikte_of_Denmark
  AddTriple (8e4313a8-117f-448d-a61a-55dafa25ce28)
 Call ID: 8e4313a8-117f-448d-a61a-55dafa25ce28
  Args:
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    target: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
    relation: :isChildOf
  AssignClass (8bf140d5-5e08-491e-bad9-56472330be90)
 Call ID: 8bf140d5-5e08-491e-bad9-56472330be90
  Args:
    source: Queen_Margrethe_II_of_Denmark
    type: :Woman
  AssignClass (8642c259-1f6f-4e0c-ae41-de555320617f)
 Call ID: 8642c259-1f6f-4e0c-ae41-de555320617f
  Args:
    type: :Person
    source: Queen_Margrethe_II_of_Denmark
  AssignClass (418fc147-15b4-4ea7-8e9b-cf8cf449a048)
 Call ID: 418fc147-15b4-4ea7-8e9b-cf8cf449a048
  Args:
    source: King_Constantine_II_of_Greece
    type: :Man
  AssignClass (512f1e76-1e0f-4b86-a772-66f31957cbe4)
 Call ID: 512f1e76-1e0f-4b86-a772-66f31957cbe4
  Args:
    type: :Person
    source: King_Constantine_II_of_Greece
  AssignClass (f5d79096-f04e-4664-ab27-0fcf33cde3b2)
 Call ID: f5d79096-f04e-4664-ab27-0fcf33cde3b2
  Args:
    source: King_Frederik_X_of_Denmark
    type: :Man
  AssignClass (0bdba7d7-b23c-4dee-a69a-8933823e0531)
 Call ID: 0bdba7d7-b23c-4dee-a69a-8933823e0531
  Args:
    type: :Person
    source: King_Frederik_X_of_Denmark
  AssignClass (ee4e7dd3-b106-494d-93a2-7727af43d46f)
 Call ID: ee4e7dd3-b106-494d-93a2-7727af43d46f
  Args:
    type: :Woman
    source: Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (0d7d2234-15b7-4a1d-88b4-39ad46bcb44d)
 Call ID: 0d7d2234-15b7-4a1d-88b4-39ad46bcb44d
  Args:
    source: Alexandra_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AddTriple (2f9d0a41-3414-4c8f-ad93-dee99e27f05c)
 Call ID: 2f9d0a41-3414-4c8f-ad93-dee99e27f05c
  Args:
    target: Alexandra_of_Sayn-Wittgenstein-Berleburg
    relation: :isSiblingOf
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
  AssignClass (78dba5e6-de3f-4210-ac69-bbb7ba10e8ae)
 Call ID: 78dba5e6-de3f-4210-ac69-bbb7ba10e8ae
  Args:
    source: Alexander_Johannsmann
    type: :Man
  AssignClass (f2608c66-ff11-4f93-bd9f-0defb7a2c17b)
 Call ID: f2608c66-ff11-4f93-bd9f-0defb7a2c17b
  Args:
    source: Alexander_Johannsmann
    type: :Person
  AddLiteral (2b0a7b5e-73f7-40e0-9143-36086b9a88a3)
 Call ID: 2b0a7b5e-73f7-40e0-9143-36086b9a88a3
  Args:
    relation: :hasBirthYear
    literal_value: 1977
    source: Alexander_Johannsmann
    literal_type: xsd:integer
  AssignClass (4876720c-3659-4191-81ca-7c3611b50c32)
 Call ID: 4876720c-3659-4191-81ca-7c3611b50c32
  Args:
    type: :Man
    source: Heinrich-Wilhelm_Johannsmann
  AssignClass (09771ddc-6f16-4984-94d9-87d705a64d14)
 Call ID: 09771ddc-6f16-4984-94d9-87d705a64d14
  Args:
    source: Heinrich-Wilhelm_Johannsmann
    type: :Person
  AddTriple (7143b217-892d-4198-b458-0f754a4361af)
 Call ID: 7143b217-892d-4198-b458-0f754a4361af
  Args:
    source: Alexander_Johannsmann
    target: Heinrich-Wilhelm_Johannsmann
    relation: :isChildOf
  AssignClass (2fdebe90-85e0-4a89-a652-ceea71e90095)
 Call ID: 2fdebe90-85e0-4a89-a652-ceea71e90095
  Args:
    type: :Man
    source: Konstantin_Gustav_Heinrich_Richard
  AssignClass (fe699fd6-a046-4628-a550-ee20320aeea1)
 Call ID: fe699fd6-a046-4628-a550-ee20320aeea1
  Args:
    type: :Person
    source: Konstantin_Gustav_Heinrich_Richard
  AddTriple (d04b23fb-620f-407a-b591-02337203a853)
 Call ID: d04b23fb-620f-407a-b591-02337203a853
  Args:
    target: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    relation: :isChildOf
    source: Konstantin_Gustav_Heinrich_Richard
  AddTriple (afca5f2a-a548-4429-a65c-b10cc5c669ce)
 Call ID: afca5f2a-a548-4429-a65c-b10cc5c669ce
  Args:
    source: Konstantin_Gustav_Heinrich_Richard
    relation: :isChildOf
    target: Alexander_Johannsmann
  AssignClass (a2881847-1ee2-42a8-a84b-899ddee636e5)
 Call ID: a2881847-1ee2-42a8-a84b-899ddee636e5
  Args:
    source: Louisa_Margareta_Benedikte_Hanna
    type: :Woman
  AssignClass (2b6ba127-aca1-46e9-a70a-c917105ddfb8)
 Call ID: 2b6ba127-aca1-46e9-a70a-c917105ddfb8
  Args:
    type: :Person
    source: Louisa_Margareta_Benedikte_Hanna
  AddTriple (45085dc2-f750-483e-b196-308d387beda9)
 Call ID: 45085dc2-f750-483e-b196-308d387beda9
  Args:
    source: Louisa_Margareta_Benedikte_Hanna
    target: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    relation: :isChildOf
  AddTriple (1c4e82e1-e37c-4e7c-a0ac-8711afd0a779)
 Call ID: 1c4e82e1-e37c-4e7c-a0ac-8711afd0a779
  Args:
    relation: :isChildOf
    target: Alexander_Johannsmann
    source: Louisa_Margareta_Benedikte_Hanna
  AssignClass (34776ac5-eb4f-4252-a110-2387f702a2ef)
 Call ID: 34776ac5-eb4f-4252-a110-2387f702a2ef
  Args:
    source: Ann-Kathrin_Johannsmann
    type: :Woman
  AssignClass (0948e505-f686-4905-9d9d-2039c8c94f10)
 Call ID: 0948e505-f686-4905-9d9d-2039c8c94f10
  Args:
    type: :Person
    source: Ann-Kathrin_Johannsmann
  AssignClass (0db66701-9d90-4188-a1b1-545ac47b8b67)
 Call ID: 0db66701-9d90-4188-a1b1-545ac47b8b67
  Args:
    type: :Man
    source: Prince_Gustav
  AssignClass (a4d1a81b-8a01-49b7-9394-20cd15f0f631)
 Call ID: a4d1a81b-8a01-49b7-9394-20cd15f0f631
  Args:
    type: :Person
    source: Prince_Gustav
  Finish (82838c49-c33d-414c-9966-34f690f9f00f)
 Call ID: 82838c49-c33d-414c-9966-34f690f9f00f
  Args: