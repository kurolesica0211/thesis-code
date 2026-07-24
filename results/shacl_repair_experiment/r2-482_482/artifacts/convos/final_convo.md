================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### CRITICAL CORE DIRECTIVES (ZERO TOLERANCE)
1. **STRICT FAITHFULNESS TO TEXT**: You are a "clean slate" engineer. Even if you recognize an entity and know more about it from your training data, you MUST NOT add any node, property, or relation that is not stated in the **Input Text**. If a fact is not in the text, it does not exist.
2. **HARD BATCH LIMIT**: You must plan your edits efficiently. **DO NOT EXCEED 20 TOOL CALLS IN A SINGLE ANSWER.** Breaking this limit is a critical system failure. Quality and strict grounding must be achieved within this budget.

### Standardized Identifier & Naming Conventions
To ensure clean downstream entity resolution, all identifiers must follow a uniform, relational-free structure.

#### 1. Core Structural Format
* **Full Formal Name**: Use the most complete, standard name mentioned *within the text* as the identifier basis.
* **Format**: Use `Snake_Case` for all entity identifiers, capitalizing the first letter of each word (e.g., `Julius_Caesar`, `Marcus_Aurelius`).
* **Avoid Pronouns/Aliases**: Never create nodes based on pronouns (`he`, `she`) or temporary descriptions (`the_captain`). Resolve these back to their primary full identifier.

#### 2. NO Relational Suffixes (ABSOLUTE PROHIBITION)
* **NEVER** use familial relations or structural dependencies to construct an identifier string. 
* **PROHIBITED EXAMPLES**: `John_son_of_Robert`, `Mary_daughter_of_Henry`, `Wife_of_Louis_XIV`.
* **Reasoning**: Relational data belongs strictly in the triples (`parentOf`, `spouseOf`), never in the unique node identifier. Incorporating them corrupts entity resolution pipelines.

#### 3. Monarchs, Nobility, and Historic Monickers
* **Regnal Numbers & Monickers**: Include standard regnal numbers or stable historical identifiers *only* if they are explicitly part of their formal name in the text (e.g., `Charlemagne`, `Louis_XIV`, `William_of_Orange`).

#### 4. Disambiguation & Fallbacks (When Identical Names Occur)
If two distinct entities share the exact same name within the text, append a parenthetical qualifier using *only* context provided in the source text:
* **By Role/Attribute**: `Augustus_(Emperor)` vs. `Augustus_(Ship)`.
* **By Category/Profession**: `John_(Apostle)` vs. `John_(Baptist)`.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source (Left)**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it.
* **The Target (Right)**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon.

#### 3. Handling Inverse Property Confusion
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.
* **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
* **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Validate**: Use `ValidateShacl` to check constraints.
4. **Iterate**: Address violations. If a violation (like MinCount) cannot be fixed without hallucinating data not in the text, **ignore the violation**.
5. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **ValidateShacl**: CRITICAL: ALWAYS validate your results before using Finish!
- **Finish**: CRITICAL: ALWAYS use ValidateShacl before finishing!
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Catharina-Amalia, Princess of Orange (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Dutch pronunciation: ; Catharina-Amalia Beatrix Carmen Victoria; born 7 December 2003) is the heir apparent to the throne of the Kingdom of the Netherlands, which consists of the constituent countries of Aruba, Curaçao, the Netherlands, and Sint Maarten.
Catharina-Amalia is the eldest child of King Willem-Alexander and Queen Máxima.
She has two younger sisters, Princess Alexia and Princess Ariane.
Early life

Princess Catharina-Amalia Beatrix Carmen Victoria of the Netherlands was born at 17:01 CET on 7 December 2003 in the HMC Bronovo in The Hague, the first child of the then Willem-Alexander, Prince of Orange (now king) and Princess Máxima.
Upon the public announcement of her birth, 101 salute shots were fired at four places in the Kingdom of the Netherlands: Den Helder and The Hague in the Netherlands, Willemstad in Curaçao, and Oranjestad in Aruba.
On 12 June 2004, Catharina-Amalia was baptised by the Rev. Carel ter Linden in the Great Church in The Hague.
Her godparents are her uncle Prince Constantijn, Crown Princess Victoria of Sweden, the (then) vice-president of the Council of State of the Netherlands Herman Tjeenk Willink, her mother's friend Samantha Deane, her uncle Martín Zorreguieta, and her father's friend Marc ter Haar.
Catharina-Amalia's maternal grandparents, Jorge Zorreguieta and María del Carmen Cerruti, were prohibited from attending her parents' wedding in 2002 due to Zorreguieta's involvement in the regime of General Jorge Rafael Videla, but were present at her baptism, which was a private rather than a state affair.
Princess Catharina-Amalia has two younger sisters: Princess Alexia (born in 2005) and Princess Ariane (born in 2007).
Her birthdays are traditionally celebrated with a concert at the Kloosterkerk in The Hague, which is attended by ambassadors and members of the royal household and the Council of State of the Netherlands.
Catharina-Amalia's paternal grandmother, Queen Beatrix, abdicated on 30 April 2013 and her father ascended the throne.
Catharina-Amalia, as the new heir apparent, assumed the title of Princess of Orange, becoming the first to do so in her own right.
Education

In December 2007, Catharina-Amalia started attending Bloemcamp Primary School, a public primary school in Wassenaar.
After graduating from primary school, she attended the Christelijk Gymnasium Sorghvliet in The Hague, where her aunt Princess Laurentien attended.
After completing her studies at Sorghvliet, Catharina-Amalia took a gap year, during which she interned at the Orange Fund and volunteered at other organisations.
Catharina-Amalia studied at the University of Amsterdam for a Bachelor of Science degree in Politics, Psychology, Law and Economics (PPLE).
In April 2024, King Willem-Alexander revealed that Catharina-Amalia lived in Madrid in 2023 under the protection of the Spanish monarchy, while she continued her studies online, due to the threats from the Moroccan mafia, a criminal organization dedicated to drug trafficking that has been threatening to kidnap her.
In August 2024, the Dutch Broadcasting Foundation announced that Catharina-Amalia joined Amsterdam corps, a Dutch student association.
Catharina-Amalia graduated with a Bachelor of Science degree in PPLE in July 2025.
Catharina-Amalia speaks Dutch, English, and Spanish (her mother's first language).
Public life

Catharina-Amalia and her sisters attended the annual Koningsdag.
On 19 June 2010, Catharina-Amalia served as a bridesmaid at the wedding of Crown Princess Victoria of Sweden and Daniel Westling.
On the occasion of her 18th birthday in 2021, a biography of Catharina-Amalia was published.
Similar books were published on the 18th birthday of Princess Beatrix in 1956 and Prince Willem-Alexander in 1985.
The book titled "Amalia" is written by Dutch entertainer Claudia de Breij.
On 8 December 2021, Catharina-Amalia assumed her seat in the Advisory Division of the Council of State when she reached the age of majority at 18 the day before.
On 17 June 2022, together with her parents, she was among the royal guests invited to the celebrations of the 18th birthday of Princess Ingrid Alexandra of Norway.
This was Catharina-Amalia's first public engagement outside of the Netherlands and the first occasion to which she was allowed to wear a tiara.
On 20 September 2022, together with her parents, Catharina-Amalia attended Prinsjesdag, where the King addressed a joint session of the States General of the Netherlands to outline government policy for the upcoming parliamentary session.
In November 2022, Catharina-Amalia and her family visited an exhibition at Nieuwe Kerk dedicated to Queen Juliana.
In January and February 2023, Catharina-Amalia went on a tour of the Dutch Caribbean with her parents.
In April 2023, Catharina-Amalia and her sister Princess Ariane attended King's Day concert in Rotterdam.
On 5 May 2023, she accompanied her grandmother to a reception held at Buckingham Palace the evening before the coronation of King Charles III and Queen Camilla of the United Kingdom.
Catharina-Amalia attended her first state banquet, honouring King Felipe VI and Queen Letizia of Spain, in April 2024.
In June 2025, Catharina-Amalia underwent surgery after falling from a horse and fracturing her arm.
Public image

Catharina-Amalia has experienced repeated fat shaming by tabloids and on social media since she was young, most notably by the Portuguese celebrity magazine Caras labeling her as plus size.
In response to the body shaming, members of the public have expressed their support for the princess, calling the fat shaming against her unacceptable.
Annual allowance

Catharina-Amalia became entitled to an annual allowance from the Dutch state upon reaching the age of 18.
Following her high school graduation, Catharina-Amalia opted to decline the annual allowance until she completed her studies.
In May 2024, citing changed circumstances, Catharina-Amalia announced she would begin utilizing her annual allowance for staff and operational expenses, starting in January 2025.
Titles, styles, honours and arms

Titles

Honours

National

Foreign

Honorific eponyms

Geographic locations

Structures

Other

Arms

See also

Notes

References

External links

2 also Princess of Lippe-Biesterfeld



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
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix data: <http://example.org/data/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

data:Catharina-Amalia a :Person,
        :Woman ;
    :hasBirthYear 2003 ;
    :hasFather data:JorgeZorreguieta,
        data:Willem-Alexander ;
    :hasMother data:M%C3%A1xima,
        data:Mar%C3%ADaDelCarmenCerruti ;
    :hasSister data:Alexia,
        data:Ariane .

data:Constantijn a :Man,
        :Person ;
    :isBrotherOf data:Willem-Alexander .

data:Mart%C3%ADnZorreguieta a :Man,
        :Person ;
    :isBrotherOf data:M%C3%A1xima .

data:Alexia a :Person,
        :Woman .

data:Ariane a :Person,
        :Woman .

data:JorgeZorreguieta a :Man,
        :Person .

data:Mar%C3%ADaDelCarmenCerruti a :Person,
        :Woman .

data:Beatrix a :Person,
        :Woman .

data:M%C3%A1xima a :Person,
        :Woman .

data:Willem-Alexander a :Man,
        :Person ;
    :hasFather data:Beatrix ;
    :hasMother data:Beatrix .



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  RemoveTriple (b6657741-df19-47ae-8fb6-5ced0f376364)
 Call ID: b6657741-df19-47ae-8fb6-5ced0f376364
  Args:
    relation: :hasFather
    source: data:Willem-Alexander
    target: data:Beatrix

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Catharina-Amalia a :Person,
          :Woman ;
      :hasBirthYear 2003 ;
      :hasFather data:JorgeZorreguieta,
          data:Willem-Alexander ;
      :hasMother data:M%C3%A1xima,
          data:Mar%C3%ADaDelCarmenCerruti ;
      :hasSister data:Alexia,
          data:Ariane .

  data:Constantijn a :Man,
          :Person ;
      :isBrotherOf data:Willem-Alexander .

  data:Mart%C3%ADnZorreguieta a :Man,
          :Person ;
      :isBrotherOf data:M%C3%A1xima .

  data:Alexia a :Person,
          :Woman .

  data:Ariane a :Person,
          :Woman .

  data:Beatrix a :Person,
          :Woman .

  data:JorgeZorreguieta a :Man,
          :Person .

  data:Mar%C3%ADaDelCarmenCerruti a :Person,
          :Woman .

  data:M%C3%A1xima a :Person,
          :Woman .

  data:Willem-Alexander a :Man,
          :Person ;
      :hasMother data:Beatrix .



================================== Ai Message ==================================

[]
Tool Calls:
  RemoveTriple (f4500e5a-6efa-4f39-8eff-2af165cfedc2)
 Call ID: f4500e5a-6efa-4f39-8eff-2af165cfedc2
  Args:
    source: data:Catharina-Amalia
    relation: :hasFather
    target: data:JorgeZorreguieta

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Catharina-Amalia a :Person,
          :Woman ;
      :hasBirthYear 2003 ;
      :hasFather data:Willem-Alexander ;
      :hasMother data:M%C3%A1xima,
          data:Mar%C3%ADaDelCarmenCerruti ;
      :hasSister data:Alexia,
          data:Ariane .

  data:Constantijn a :Man,
          :Person ;
      :isBrotherOf data:Willem-Alexander .

  data:JorgeZorreguieta a :Man,
          :Person .

  data:Mart%C3%ADnZorreguieta a :Man,
          :Person ;
      :isBrotherOf data:M%C3%A1xima .

  data:Alexia a :Person,
          :Woman .

  data:Ariane a :Person,
          :Woman .

  data:Beatrix a :Person,
          :Woman .

  data:Mar%C3%ADaDelCarmenCerruti a :Person,
          :Woman .

  data:M%C3%A1xima a :Person,
          :Woman .

  data:Willem-Alexander a :Man,
          :Person ;
      :hasMother data:Beatrix .



================================== Ai Message ==================================

[]
Tool Calls:
  RemoveTriple (89f182f8-d926-4652-a45b-64c8efea46d1)
 Call ID: 89f182f8-d926-4652-a45b-64c8efea46d1
  Args:
    source: data:Catharina-Amalia
    relation: :hasMother
    target: data:Mar%C3%ADaDelCarmenCerruti

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Catharina-Amalia a :Person,
          :Woman ;
      :hasBirthYear 2003 ;
      :hasFather data:Willem-Alexander ;
      :hasMother data:M%C3%A1xima ;
      :hasSister data:Alexia,
          data:Ariane .

  data:Constantijn a :Man,
          :Person ;
      :isBrotherOf data:Willem-Alexander .

  data:JorgeZorreguieta a :Man,
          :Person .

  data:Mar%C3%ADaDelCarmenCerruti a :Person,
          :Woman .

  data:Mart%C3%ADnZorreguieta a :Man,
          :Person ;
      :isBrotherOf data:M%C3%A1xima .

  data:Alexia a :Person,
          :Woman .

  data:Ariane a :Person,
          :Woman .

  data:Beatrix a :Person,
          :Woman .

  data:M%C3%A1xima a :Person,
          :Woman .

  data:Willem-Alexander a :Man,
          :Person ;
      :hasMother data:Beatrix .



================================== Ai Message ==================================

[]
Tool Calls:
  AddTriple (3d9090d6-d0c6-4290-b726-ae4a72242e43)
 Call ID: 3d9090d6-d0c6-4290-b726-ae4a72242e43
  Args:
    target: data:M%C3%A1xima
    source: data:JorgeZorreguieta
    relation: :isFatherOf

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Catharina-Amalia a :Person,
          :Woman ;
      :hasBirthYear 2003 ;
      :hasFather data:Willem-Alexander ;
      :hasMother data:M%C3%A1xima ;
      :hasSister data:Alexia,
          data:Ariane .

  data:Constantijn a :Man,
          :Person ;
      :isBrotherOf data:Willem-Alexander .

  data:JorgeZorreguieta a :Man,
          :Person ;
      :isFatherOf data:M%C3%A1xima .

  data:Mar%C3%ADaDelCarmenCerruti a :Person,
          :Woman .

  data:Mart%C3%ADnZorreguieta a :Man,
          :Person ;
      :isBrotherOf data:M%C3%A1xima .

  data:Alexia a :Person,
          :Woman .

  data:Ariane a :Person,
          :Woman .

  data:Beatrix a :Person,
          :Woman .

  data:Willem-Alexander a :Man,
          :Person ;
      :hasMother data:Beatrix .

  data:M%C3%A1xima a :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AddTriple (1f506930-8f57-4654-aa1e-76c0fc37a166)
 Call ID: 1f506930-8f57-4654-aa1e-76c0fc37a166
  Args:
    source: data:Mar%C3%ADaDelCarmenCerruti
    target: data:M%C3%A1xima
    relation: :isMotherOf

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Catharina-Amalia a :Person,
          :Woman ;
      :hasBirthYear 2003 ;
      :hasFather data:Willem-Alexander ;
      :hasMother data:M%C3%A1xima ;
      :hasSister data:Alexia,
          data:Ariane .

  data:Constantijn a :Man,
          :Person ;
      :isBrotherOf data:Willem-Alexander .

  data:JorgeZorreguieta a :Man,
          :Person ;
      :isFatherOf data:M%C3%A1xima .

  data:Mar%C3%ADaDelCarmenCerruti a :Person,
          :Woman ;
      :isMotherOf data:M%C3%A1xima .

  data:Mart%C3%ADnZorreguieta a :Man,
          :Person ;
      :isBrotherOf data:M%C3%A1xima .

  data:Alexia a :Person,
          :Woman .

  data:Ariane a :Person,
          :Woman .

  data:Beatrix a :Person,
          :Woman .

  data:Willem-Alexander a :Man,
          :Person ;
      :hasMother data:Beatrix .

  data:M%C3%A1xima a :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (78fb99b6-adef-4878-bf2a-5859172db865)
 Call ID: 78fb99b6-adef-4878-bf2a-5859172db865
  Args:

================================= Tool Message =================================

VALIDATION RESULTS
Total violations:11
Violations:

  Violation [1]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node 'Willem-Alexander' used as the 'hasFather' for 'Catharina-Amalia' is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Willem-Alexander', class=':Ancestor')


  Violation [2]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'M%C3%A1xima' used as the 'hasMother' for 'Catharina-Amalia' is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='M%C3%A1xima', class=':Ancestor')


  Violation [3]:
    SHACL message: Any subject of isFatherOf must be all of: Ancestor, Man.
    LLM-provided explanation of the violation:
      The node 'JorgeZorreguieta' is involved in an 'isFatherOf' relationship but is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='JorgeZorreguieta', class=':Ancestor')


  Violation [4]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'Beatrix' used as the 'hasMother' for 'Willem-Alexander' is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Beatrix', class=':Ancestor')


  Violation [5]:
    SHACL message: Any subject of isMotherOf must be all of: Ancestor, Woman.
    LLM-provided explanation of the violation:
      The node 'Mar%C3%ADaDelCarmenCerruti' is involved in an 'isMotherOf' relationship but is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Mar%C3%ADaDelCarmenCerruti', class=':Ancestor')


  Violation [6]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node 'Willem-Alexander' is already identified as a ':Man', but the validation requires it to also possess the ':Ancestor' class for the 'hasFather' property.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Willem-Alexander', class=':Ancestor')


  Violation [7]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'M%C3%A1xima' is already identified as a ':Woman', but the validation requires it to also possess the ':Ancestor' class for the 'hasMother' property.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='M%C3%A1xima', class=':Ancestor')


  Violation [8]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'Beatrix' is already identified as a ':Woman', but the validation requires it to also possess the ':Ancestor' class for the 'hasMother' property.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Beatrix', class=':Ancestor')


  Violation [9]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node 'Willem-Alexander' is missing the ':Ancestor' class assignment required for the 'hasFather' relationship.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Willem-Alexander', class=':Ancestor')


  Violation [10]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'M%C3%A1xima' is missing the ':Ancestor' class assignment required for the 'hasMother' relationship.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='M%C3%A1xima', class=':Ancestor')


  Violation [11]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'Beatrix' is missing the ':Ancestor' class assignment required for the 'hasMother' relationship.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Beatrix', class=':Ancestor')




================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (341bb278-a20d-4e59-af74-c03453269d68)
 Call ID: 341bb278-a20d-4e59-af74-c03453269d68
  Args:
    source: data:Willem-Alexander
    type: :Ancestor

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Catharina-Amalia a :Person,
          :Woman ;
      :hasBirthYear 2003 ;
      :hasFather data:Willem-Alexander ;
      :hasMother data:M%C3%A1xima ;
      :hasSister data:Alexia,
          data:Ariane .

  data:Constantijn a :Man,
          :Person ;
      :isBrotherOf data:Willem-Alexander .

  data:JorgeZorreguieta a :Man,
          :Person ;
      :isFatherOf data:M%C3%A1xima .

  data:Mar%C3%ADaDelCarmenCerruti a :Person,
          :Woman ;
      :isMotherOf data:M%C3%A1xima .

  data:Mart%C3%ADnZorreguieta a :Man,
          :Person ;
      :isBrotherOf data:M%C3%A1xima .

  data:Alexia a :Person,
          :Woman .

  data:Ariane a :Person,
          :Woman .

  data:Beatrix a :Person,
          :Woman .

  data:Willem-Alexander a :Ancestor,
          :Man,
          :Person ;
      :hasMother data:Beatrix .

  data:M%C3%A1xima a :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (86378d56-8482-41d6-ba6f-b0f78f45ca76)
 Call ID: 86378d56-8482-41d6-ba6f-b0f78f45ca76
  Args:
    type: :Ancestor
    source: data:M%C3%A1xima

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Catharina-Amalia a :Person,
          :Woman ;
      :hasBirthYear 2003 ;
      :hasFather data:Willem-Alexander ;
      :hasMother data:M%C3%A1xima ;
      :hasSister data:Alexia,
          data:Ariane .

  data:Constantijn a :Man,
          :Person ;
      :isBrotherOf data:Willem-Alexander .

  data:JorgeZorreguieta a :Man,
          :Person ;
      :isFatherOf data:M%C3%A1xima .

  data:Mar%C3%ADaDelCarmenCerruti a :Person,
          :Woman ;
      :isMotherOf data:M%C3%A1xima .

  data:Mart%C3%ADnZorreguieta a :Man,
          :Person ;
      :isBrotherOf data:M%C3%A1xima .

  data:Alexia a :Person,
          :Woman .

  data:Ariane a :Person,
          :Woman .

  data:Beatrix a :Person,
          :Woman .

  data:Willem-Alexander a :Ancestor,
          :Man,
          :Person ;
      :hasMother data:Beatrix .

  data:M%C3%A1xima a :Ancestor,
          :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (2b090b58-a840-4cbe-a39b-595ffe35a973)
 Call ID: 2b090b58-a840-4cbe-a39b-595ffe35a973
  Args:
    type: :Ancestor
    source: data:JorgeZorreguieta

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Catharina-Amalia a :Person,
          :Woman ;
      :hasBirthYear 2003 ;
      :hasFather data:Willem-Alexander ;
      :hasMother data:M%C3%A1xima ;
      :hasSister data:Alexia,
          data:Ariane .

  data:Constantijn a :Man,
          :Person ;
      :isBrotherOf data:Willem-Alexander .

  data:JorgeZorreguieta a :Ancestor,
          :Man,
          :Person ;
      :isFatherOf data:M%C3%A1xima .

  data:Mar%C3%ADaDelCarmenCerruti a :Person,
          :Woman ;
      :isMotherOf data:M%C3%A1xima .

  data:Mart%C3%ADnZorreguieta a :Man,
          :Person ;
      :isBrotherOf data:M%C3%A1xima .

  data:Alexia a :Person,
          :Woman .

  data:Ariane a :Person,
          :Woman .

  data:Beatrix a :Person,
          :Woman .

  data:Willem-Alexander a :Ancestor,
          :Man,
          :Person ;
      :hasMother data:Beatrix .

  data:M%C3%A1xima a :Ancestor,
          :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (60a441fd-360c-4170-b44e-0f87b0267eda)
 Call ID: 60a441fd-360c-4170-b44e-0f87b0267eda
  Args:
    source: data:Beatrix
    type: :Ancestor

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Catharina-Amalia a :Person,
          :Woman ;
      :hasBirthYear 2003 ;
      :hasFather data:Willem-Alexander ;
      :hasMother data:M%C3%A1xima ;
      :hasSister data:Alexia,
          data:Ariane .

  data:Constantijn a :Man,
          :Person ;
      :isBrotherOf data:Willem-Alexander .

  data:JorgeZorreguieta a :Ancestor,
          :Man,
          :Person ;
      :isFatherOf data:M%C3%A1xima .

  data:Mar%C3%ADaDelCarmenCerruti a :Person,
          :Woman ;
      :isMotherOf data:M%C3%A1xima .

  data:Mart%C3%ADnZorreguieta a :Man,
          :Person ;
      :isBrotherOf data:M%C3%A1xima .

  data:Alexia a :Person,
          :Woman .

  data:Ariane a :Person,
          :Woman .

  data:Beatrix a :Ancestor,
          :Person,
          :Woman .

  data:Willem-Alexander a :Ancestor,
          :Man,
          :Person ;
      :hasMother data:Beatrix .

  data:M%C3%A1xima a :Ancestor,
          :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (029e3373-92a4-4bf3-ae30-7bddb2ab118c)
 Call ID: 029e3373-92a4-4bf3-ae30-7bddb2ab118c
  Args:
    type: :Ancestor
    source: data:Mar%C3%ADaDelCarmenCerruti

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Catharina-Amalia a :Person,
          :Woman ;
      :hasBirthYear 2003 ;
      :hasFather data:Willem-Alexander ;
      :hasMother data:M%C3%A1xima ;
      :hasSister data:Alexia,
          data:Ariane .

  data:Constantijn a :Man,
          :Person ;
      :isBrotherOf data:Willem-Alexander .

  data:JorgeZorreguieta a :Ancestor,
          :Man,
          :Person ;
      :isFatherOf data:M%C3%A1xima .

  data:Mar%C3%ADaDelCarmenCerruti a :Ancestor,
          :Person,
          :Woman ;
      :isMotherOf data:M%C3%A1xima .

  data:Mart%C3%ADnZorreguieta a :Man,
          :Person ;
      :isBrotherOf data:M%C3%A1xima .

  data:Alexia a :Person,
          :Woman .

  data:Ariane a :Person,
          :Woman .

  data:Beatrix a :Ancestor,
          :Person,
          :Woman .

  data:Willem-Alexander a :Ancestor,
          :Man,
          :Person ;
      :hasMother data:Beatrix .

  data:M%C3%A1xima a :Ancestor,
          :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (acb891ad-601b-43d0-88fb-f1cdc5927d89)
 Call ID: acb891ad-601b-43d0-88fb-f1cdc5927d89
  Args:

================================= Tool Message =================================

SHACL validation has not produced any violations.

================================== Ai Message ==================================

[]
Tool Calls:
  Finish (7c12a8ab-a58b-4954-a2c1-0d2348ae3587)
 Call ID: 7c12a8ab-a58b-4954-a2c1-0d2348ae3587
  Args: