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
Prince Christopher of Greece and Denmark (Greek: Χριστόφορος, romanized: Christóphoros; 10 August 1888 – 21 January 1940) was the fifth and youngest son and youngest child of King George I of Greece, belonging to a dynasty which mounted and lost the throne of Greece several times during his lifetime.
Family background

Christopher was born at Pavlovsk, Imperial Russia, son of King George I of Greece and Queen Olga, a Russian grand duchess by birth.
He was called "Christo" in the family.
His older brothers were future King Constantine I, George, Nicholas and Andrew.
Christopher, like his siblings, was a polyglot, speaking Greek, English, Danish, Russian, French, and Italian.
The Hellenic royal line was a cadet branch of the Schleswig-Holstein-Sonderburg-Glücksburg dynasty which had mounted the throne of Greece in 1863.
Early adulthood

When Christopher came of age he joined the Hellenic Navy, although apparently he would rather have studied the piano.
He was briefly engaged to Princess Alexandra, 2nd Duchess of Fife in about 1910 (Alexandra's mother, Princess Louise, Duchess of Fife, was a daughter of King Edward VII and Queen Alexandra of the United Kingdom, herself an older sister of George I of Greece, Christopher's father).
First marriage

On 1 January 1920, Christopher married a very wealthy American widow, Nonnie May "Nancy" Stewart Worthington Leeds, at Vevey, Switzerland.
His bride, a once-divorced and once-widowed commoner at least a decade older than the prince, was nonetheless recognised as Christopher's dynastic wife by his family (at the time of the engagement and wedding, the Greek royal family lived frugally in exile, and as Christopher was last in the dynasty's order of succession, any children he fathered would not impact the succession rights of other Greek dynasts).
Shortly after their marriage, Princess Anastasia developed cancer, and died in London on 29 August 1923, leaving no children from this marriage.
Prince Christopher did, however, have a stepson, William Bateman Leeds Jr (1902–1971), who had, in 1921, married Princess Xenia Georgievna of Russia.
She was Christopher's niece through his elder sister, Marie of Greece, Grand Duchess George of Russia.
Second marriage and family

Prince Christopher later remarried; his second wife was Princess Françoise of Orléans (25 December 1902 – 25 February 1953).
Françoise was a daughter of Jean d'Orléans, Duc de Guise, Orléanist pretender to the throne of France, by his wife/first cousin, Isabelle d'Orléans.
Isabelle was, in turn, a daughter of Philippe, Comte de Paris by his wife and first cousin, Infanta Isabel de Orléans y Borbon.
They were childless for a decade, then one child was born to Françoise: Prince Michael of Greece and Denmark was born in Rome in 1939, shortly before Prince Christopher's death.
Opinion on Anna Anderson

In 1927, Prince Christopher paid a visit to the Long Island home of William and Xenia Leeds, respectively his stepson and niece.
Xenia had taken an interest in the strange case of a woman, Anna Anderson, who claimed to be Grand Duchess Anastasia Nikolaevna of Russia, the youngest daughter of the last Tsar of Russia, Nicholas II.
As Prince Christopher explained, "That was her story, and, fantastic as it was, there were many who believed then − and still believe − in her, among them one or two members of the Imperial Family."
Prince Christopher described her: "In the first place she was unable to speak Russian, which the Grand Duchess Anastasia, like all the Czar's children, had talked fluently − and would only converse in German.
Opinion on monarchy

Prince Christopher recorded his thoughts on monarchy and those aspiring to it: "Nothing under the sun would induce me to accept a Kingdom.
"


Death

Prince Christopher of Greece died in Athens on 21 January 1940, aged 51.



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
  AssignClass (3aeb654d-bde6-4708-a71d-c2753f793a5f)
 Call ID: 3aeb654d-bde6-4708-a71d-c2753f793a5f
  Args:
    type: :Man
    source: :PrinceChristopherOfGreeceAndDenmark
  AssignClass (b1af4255-029f-44fb-95d5-0fe22e594f1f)
 Call ID: b1af4255-029f-44fb-95d5-0fe22e594f1f
  Args:
    source: :KingGeorgeIOfGreece
    type: :Man
  AssignClass (e992de91-de41-4e42-b878-f078565c9780)
 Call ID: e992de91-de41-4e42-b878-f078565c9780
  Args:
    source: :QueenOlga
    type: :Woman
  AddLiteral (d9ec2c29-9fa9-4f40-870a-4429e110792a)
 Call ID: d9ec2c29-9fa9-4f40-870a-4429e110792a
  Args:
    literal_type: xsd:integer
    source: :PrinceChristopherOfGreeceAndDenmark
    literal_value: 1888
    relation: :hasBirthYear
  AddLiteral (934c0224-da2a-4276-8d7a-7c444a0ccf47)
 Call ID: 934c0224-da2a-4276-8d7a-7c444a0ccf47
  Args:
    relation: :hasDeathYear
    literal_value: 1940
    source: :PrinceChristopherOfGreeceAndDenmark
    literal_type: xsd:integer
  AddTriple (07ea8ab6-be34-43c7-bd19-74ece3379896)
 Call ID: 07ea8ab6-be34-43c7-bd19-74ece3379896
  Args:
    source: :PrinceChristopherOfGreeceAndDenmark
    relation: :hasFather
    target: :KingGeorgeIOfGreece
  AddTriple (45ea46ad-6fc6-44b8-8eac-0c465a4f4da5)
 Call ID: 45ea46ad-6fc6-44b8-8eac-0c465a4f4da5
  Args:
    source: :PrinceChristopherOfGreeceAndDenmark
    relation: :hasMother
    target: :QueenOlga
  AddLiteral (92d3f9e4-6928-4f88-b4fc-5cf9c6e6a9a5)
 Call ID: 92d3f9e4-6928-4f88-b4fc-5cf9c6e6a9a5
  Args:
    literal_type: xsd:string
    source: :PrinceChristopherOfGreeceAndDenmark
    relation: :knownAs
    literal_value: Christo
  AddTriple (f6f5aca5-6a61-46b8-be79-4a5bd8aec744)
 Call ID: f6f5aca5-6a61-46b8-be79-4a5bd8aec744
  Args:
    source: :PrinceChristopherOfGreeceAndDenmark
    target: :KingConstantineI
    relation: :hasBrother
  AddTriple (fa26f7e8-417d-4081-aff7-f5d9952a03e1)
 Call ID: fa26f7e8-417d-4081-aff7-f5d9952a03e1
  Args:
    source: :PrinceChristopherOfGreeceAndDenmark
    target: :PrinceGeorge
    relation: :hasBrother
  AddTriple (8a5f0874-c0c2-425c-b040-147eb5696fcb)
 Call ID: 8a5f0874-c0c2-425c-b040-147eb5696fcb
  Args:
    source: :PrinceChristopherOfGreeceAndDenmark
    target: :PrinceNicholas
    relation: :hasBrother
  AddTriple (bb84e303-0a45-4a16-8883-2b7eea73e315)
 Call ID: bb84e303-0a45-4a16-8883-2b7eea73e315
  Args:
    source: :PrinceChristopherOfGreeceAndDenmark
    target: :PrinceAndrew
    relation: :hasBrother
  AssignClass (2f039612-2b82-4e4d-a7f7-a960ea604068)
 Call ID: 2f039612-2b82-4e4d-a7f7-a960ea604068
  Args:
    source: :KingConstantineI
    type: :Man
  AssignClass (245bc564-faa8-4fe6-bcb3-fdfa7dd2ce90)
 Call ID: 245bc564-faa8-4fe6-bcb3-fdfa7dd2ce90
  Args:
    type: :Man
    source: :PrinceGeorge
  AssignClass (71a37375-ea46-4238-b6b8-7858a1edadc8)
 Call ID: 71a37375-ea46-4238-b6b8-7858a1edadc8
  Args:
    source: :PrinceNicholas
    type: :Man
  AssignClass (ec6aff57-eadd-4428-a403-31b99b605bd4)
 Call ID: ec6aff57-eadd-4428-a403-31b99b605bd4
  Args:
    type: :Man
    source: :PrinceAndrew
  AddTriple (047475ec-56d1-426a-91ff-2a20fb61fc4e)
 Call ID: 047475ec-56d1-426a-91ff-2a20fb61fc4e
  Args:
    relation: :hasMother
    target: :PrincessFrancoiseOfOrleans
    source: :PrinceMichaelOfGreeceAndDenmark
  AddTriple (1d08324d-80f6-4ab8-ab56-89645ecf47cc)
 Call ID: 1d08324d-80f6-4ab8-ab56-89645ecf47cc
  Args:
    relation: :hasFather
    target: :PrinceChristopherOfGreeceAndDenmark
    source: :PrinceMichaelOfGreeceAndDenmark
  AssignClass (92fe458e-58a6-4432-a97d-26559a63937d)
 Call ID: 92fe458e-58a6-4432-a97d-26559a63937d
  Args:
    source: :PrinceMichaelOfGreeceAndDenmark
    type: :Man
  AssignClass (3bb1f8d8-8e4d-490c-b7fe-313cba8ea6ab)
 Call ID: 3bb1f8d8-8e4d-490c-b7fe-313cba8ea6ab
  Args:
    source: :PrincessFrancoiseOfOrleans
    type: :Woman
  AddLiteral (56731135-e67e-4314-8474-238364561bcf)
 Call ID: 56731135-e67e-4314-8474-238364561bcf
  Args:
    literal_type: xsd:integer
    source: :PrinceMichaelOfGreeceAndDenmark
    literal_value: 1939
    relation: :hasBirthYear
  AddTriple (4df31238-cd3c-4d6c-b5a2-bfce27a18771)
 Call ID: 4df31238-cd3c-4d6c-b5a2-bfce27a18771
  Args:
    target: :JeanDOrleans
    relation: :hasFather
    source: :PrincessFrancoiseOfOrleans
  AddTriple (ff763c16-2285-4131-b92e-35434bcc38f7)
 Call ID: ff763c16-2285-4131-b92e-35434bcc38f7
  Args:
    source: :PrincessFrancoiseOfOrleans
    relation: :hasMother
    target: :IsabelleDOrleans
  AssignClass (a3931f4d-943a-4ddb-9f9a-127e2f575fc0)
 Call ID: a3931f4d-943a-4ddb-9f9a-127e2f575fc0
  Args:
    source: :JeanDOrleans
    type: :Man
  AssignClass (a349fe7f-6ca1-4093-8348-3644f0cccec2)
 Call ID: a349fe7f-6ca1-4093-8348-3644f0cccec2
  Args:
    type: :Woman
    source: :IsabelleDOrleans
  AddTriple (d5a96dd4-ee21-4690-b6ca-7d5bed37e807)
 Call ID: d5a96dd4-ee21-4690-b6ca-7d5bed37e807
  Args:
    source: :IsabelleDOrleans
    relation: :hasFather
    target: :PhilippeComteDeParis
  AddTriple (3af7ab97-3cb4-4249-8cc8-bdf46ae4d98a)
 Call ID: 3af7ab97-3cb4-4249-8cc8-bdf46ae4d98a
  Args:
    source: :IsabelleDOrleans
    target: :InfantaIsabelDeOrleansYBorbon
    relation: :hasMother
  AssignClass (292a24bc-c0f0-4192-9cd6-b2c56894cc30)
 Call ID: 292a24bc-c0f0-4192-9cd6-b2c56894cc30
  Args:
    source: :PhilippeComteDeParis
    type: :Man
  AssignClass (b9aa8cb0-9e16-4304-8506-9bcfd375eff9)
 Call ID: b9aa8cb0-9e16-4304-8506-9bcfd375eff9
  Args:
    source: :InfantaIsabelDeOrleansYBorbon
    type: :Woman
  AddTriple (5090dfd9-bfdc-40f4-b0c2-797eee77ddfc)
 Call ID: 5090dfd9-bfdc-40f4-b0c2-797eee77ddfc
  Args:
    relation: :hasMother
    target: :MarieOfGreece
    source: :PrincessXeniaGeorgievnaOfRussia
  AssignClass (2bdf2075-0657-4dac-8a96-1a3c91df2c8d)
 Call ID: 2bdf2075-0657-4dac-8a96-1a3c91df2c8d
  Args:
    source: :PrincessXeniaGeorgievnaOfRussia
    type: :Woman
  AssignClass (7d998648-a226-41d1-90fa-909da2772728)
 Call ID: 7d998648-a226-41d1-90fa-909da2772728
  Args:
    type: :Woman
    source: :MarieOfGreece
  AddTriple (b4e6be9a-2275-48d1-8ef4-d089d9ebaf7a)
 Call ID: b4e6be9a-2275-48d1-8ef4-d089d9ebaf7a
  Args:
    target: :MarieOfGreece
    relation: :hasSister
    source: :PrinceChristopherOfGreeceAndDenmark
  Finish (7e985eed-3d0b-484a-b5f0-c0d626744ac7)
 Call ID: 7e985eed-3d0b-484a-b5f0-c0d626744ac7
  Args: