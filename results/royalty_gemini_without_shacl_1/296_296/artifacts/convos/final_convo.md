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
  AssignClass (5019019f-506e-4698-ab3e-3708a815df66)
 Call ID: 5019019f-506e-4698-ab3e-3708a815df66
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    type: :Man
  AddLiteral (46281be2-c812-41a2-94c6-4e65d4967edb)
 Call ID: 46281be2-c812-41a2-94c6-4e65d4967edb
  Args:
    literal_value: 1888
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_Christopher_of_Greece_and_Denmark
  AddLiteral (ddd762a9-2f6a-44db-add0-e7aaae99d571)
 Call ID: ddd762a9-2f6a-44db-add0-e7aaae99d571
  Args:
    literal_value: 1940
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Prince_Christopher_of_Greece_and_Denmark
  AddLiteral (9c25075e-9448-4c63-a992-80be5f35374c)
 Call ID: 9c25075e-9448-4c63-a992-80be5f35374c
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    literal_value: Christo
    source: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (5574e217-d415-4b17-9165-8e546da3670e)
 Call ID: 5574e217-d415-4b17-9165-8e546da3670e
  Args:
    type: :Man
    source: King_George_I_of_Greece
  AssignClass (b2940597-a4ff-4fdd-9556-9dc74da376a0)
 Call ID: b2940597-a4ff-4fdd-9556-9dc74da376a0
  Args:
    source: Queen_Olga_of_Greece
    type: :Woman
  AddTriple (7cf5d6df-9896-4810-9a55-7d0e0fb92c7a)
 Call ID: 7cf5d6df-9896-4810-9a55-7d0e0fb92c7a
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    relation: :hasFather
    target: King_George_I_of_Greece
  AddTriple (fbf8c238-657a-41ad-8aff-6868e3f18b8f)
 Call ID: fbf8c238-657a-41ad-8aff-6868e3f18b8f
  Args:
    relation: :hasMother
    source: Prince_Christopher_of_Greece_and_Denmark
    target: Queen_Olga_of_Greece
  AssignClass (d73fcfbe-a42a-49f3-9c65-46d1343f5109)
 Call ID: d73fcfbe-a42a-49f3-9c65-46d1343f5109
  Args:
    type: :Man
    source: Constantine_I_of_Greece
  AssignClass (f687fd0a-8c69-4d23-9951-cf6248fce054)
 Call ID: f687fd0a-8c69-4d23-9951-cf6248fce054
  Args:
    type: :Man
    source: George_of_Greece
  AssignClass (403b62d6-6397-4e1b-9f78-4fd6d60ae6c0)
 Call ID: 403b62d6-6397-4e1b-9f78-4fd6d60ae6c0
  Args:
    source: Nicholas_of_Greece
    type: :Man
  AssignClass (26370881-725c-469e-99ea-c23937ad4802)
 Call ID: 26370881-725c-469e-99ea-c23937ad4802
  Args:
    source: Andrew_of_Greece
    type: :Man
  AddTriple (2db93552-1612-46d6-90a6-1791f0175300)
 Call ID: 2db93552-1612-46d6-90a6-1791f0175300
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    relation: :isBrotherOf
    target: Constantine_I_of_Greece
  AddTriple (d6d13576-482c-4f3f-98e0-d97fea00a681)
 Call ID: d6d13576-482c-4f3f-98e0-d97fea00a681
  Args:
    target: George_of_Greece
    source: Prince_Christopher_of_Greece_and_Denmark
    relation: :isBrotherOf
  AddTriple (08a599cb-7f3d-4991-9164-aa7d58d277e0)
 Call ID: 08a599cb-7f3d-4991-9164-aa7d58d277e0
  Args:
    target: Nicholas_of_Greece
    relation: :isBrotherOf
    source: Prince_Christopher_of_Greece_and_Denmark
  AddTriple (a0a796e6-d98f-44c4-9b87-94d1ea165f58)
 Call ID: a0a796e6-d98f-44c4-9b87-94d1ea165f58
  Args:
    relation: :isBrotherOf
    source: Prince_Christopher_of_Greece_and_Denmark
    target: Andrew_of_Greece
  AssignClass (0eb9cc80-0bb8-464c-92de-d13c0bcc3b3c)
 Call ID: 0eb9cc80-0bb8-464c-92de-d13c0bcc3b3c
  Args:
    type: :Woman
    source: Marie_of_Greece
  AddTriple (3db43688-b048-43e2-a8fc-9644f7babc68)
 Call ID: 3db43688-b048-43e2-a8fc-9644f7babc68
  Args:
    target: Marie_of_Greece
    source: Prince_Christopher_of_Greece_and_Denmark
    relation: :isSisterOf
  AssignClass (b9ad5f09-4599-409f-a501-8360e21c455b)
 Call ID: b9ad5f09-4599-409f-a501-8360e21c455b
  Args:
    type: :Woman
    source: Princess_Anastasia_of_Greece
  AddTriple (b510d141-93da-44a1-97c9-dfcac9730eb6)
 Call ID: b510d141-93da-44a1-97c9-dfcac9730eb6
  Args:
    relation: :hasRelation
    source: Prince_Christopher_of_Greece_and_Denmark
    target: Princess_Anastasia_of_Greece
  AddLiteral (ea2a60dd-d68a-4d94-8311-f7da83cdbfa3)
 Call ID: ea2a60dd-d68a-4d94-8311-f7da83cdbfa3
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1920
  AssignClass (d6ca5f5c-b0d6-4efa-8f26-c25ce969dc1e)
 Call ID: d6ca5f5c-b0d6-4efa-8f26-c25ce969dc1e
  Args:
    type: :Man
    source: William_Bateman_Leeds_Jr
  AddTriple (0aced40a-a98e-491e-b1bc-8925074a8838)
 Call ID: 0aced40a-a98e-491e-b1bc-8925074a8838
  Args:
    target: William_Bateman_Leeds_Jr
    source: Prince_Christopher_of_Greece_and_Denmark
    relation: :hasRelation
  AssignClass (70cc8feb-7704-41b6-8c74-e40b4b4c6894)
 Call ID: 70cc8feb-7704-41b6-8c74-e40b4b4c6894
  Args:
    type: :Woman
    source: Princess_Francoise_of_Orleans
  AddTriple (88c09dd4-d255-4c9c-8375-c19499559f8f)
 Call ID: 88c09dd4-d255-4c9c-8375-c19499559f8f
  Args:
    relation: :hasRelation
    source: Prince_Christopher_of_Greece_and_Denmark
    target: Princess_Francoise_of_Orleans
  AssignClass (1aeb0068-eb05-441a-baaa-1737de43d119)
 Call ID: 1aeb0068-eb05-441a-baaa-1737de43d119
  Args:
    type: :Man
    source: Prince_Michael_of_Greece_and_Denmark
  AddTriple (644c2788-8606-4ec4-ba8e-f9781f424e48)
 Call ID: 644c2788-8606-4ec4-ba8e-f9781f424e48
  Args:
    target: Prince_Christopher_of_Greece_and_Denmark
    relation: :hasFather
    source: Prince_Michael_of_Greece_and_Denmark
  AddTriple (086e7876-0ee0-419f-9f96-15e3d45bfd7d)
 Call ID: 086e7876-0ee0-419f-9f96-15e3d45bfd7d
  Args:
    target: Princess_Francoise_of_Orleans
    relation: :hasMother
    source: Prince_Michael_of_Greece_and_Denmark
  Finish (9ee53abf-5450-4c50-9d66-2300917a0deb)
 Call ID: 9ee53abf-5450-4c50-9d66-2300917a0deb
  Args: